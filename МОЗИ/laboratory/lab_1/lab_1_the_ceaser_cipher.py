import streamlit as st

EXCEPTIONS = '.,?!-" '

def isRussia(letter: str) -> bool:
    return 1040 <= ord(letter) <= 1103

def encryption(text: str, k: int) -> str:
    result = ''
    for i in range(len(text)):
        letter = text[i]
        if not isRussia(letter) or letter in EXCEPTIONS:
            result += letter
            continue
        elif letter.islower():
            result += chr(ord('а') + (ord(letter) + k - ord('а')) % 32)
        else:
            result += chr(ord('А') + (ord(letter) + k - ord('А')) % 32)
    return result

def decrypt_enumeration(text):
    result = {}
    for k in range(1, 32):
        result[k] = ''
        for i in range(len(text)):
            letter = text[i]
            if not isRussia(letter) or letter in EXCEPTIONS:
                result[k] += letter
                continue
            elif letter.islower():
                result[k] += chr(ord('я') - (ord('я') - ord(letter) + k) % 32)
            else:
                result[k] += chr(ord('Я') - (ord('Я') - ord(letter) + k) % 32)
    return result

def decrypt(text: str, k: int=None):
    result = ''
    if (k is None): 
        result = decrypt_enumeration(text)
    else:
        for i in range(len(text)):
            letter = text[i]
            if not isRussia(letter) or letter in EXCEPTIONS:
                result += letter
                continue
            elif letter.islower():
                result += chr(ord('я') - (ord('я') - ord(letter) + k) % 32)
            else:
                result += chr(ord('Я') - (ord('Я') - ord(letter) + k) % 32)
    return result

def get_shift(action: str):
    if action == "Шифровка":
        shift = st.number_input(
            label='Шаг от 1 до 31',
            min_value=1, max_value=31, step=1,
            key="enc_shift"
        )
        return int(shift)
    else:
        use_step = st.checkbox("Выбрать шаг", value=False, key="dec_use_step")
        if use_step:
            shift = st.number_input(
                label='Шаг от 1 до 31',
                min_value=1, max_value=31, step=1,
                key="dec_shift"
            )
            return int(shift)
        else:
            return None

def main_page():
    st.title("Шифр Цезаря")

    if "dec_variants" not in st.session_state:
        st.session_state.dec_variants = {}
    if "last_text_for_variants" not in st.session_state:
        st.session_state.last_text_for_variants = ""

    user_text = st.text_area("Введите текст:").replace('ё', 'е').replace('Ё', 'Е')

    if user_text != st.session_state.last_text_for_variants:
        st.session_state.dec_variants = {}
        st.session_state.last_text_for_variants = user_text

    action = st.selectbox("Выберите действие:", ("Шифровка", "Расшифровка"))
    shift = get_shift(action)

    if action == "Расшифровка" and shift is not None:
        if st.button("Очистить накопленные варианты", key="clear_variants_btn"):
            st.session_state.dec_variants = {}
            st.info("Список вариантов очищен.")

    if st.button(action, key="do_action_btn"):
        file_name = None
        file_content = None

        if action == "Шифровка":
            result = encryption(user_text, shift)
            file_name = "Шифр_Цезаря_Шифровка.txt"
            file_content = (
                "Результат шифрования (Цезарь)\n"
                f"Исходный текст (ОТ):\n{user_text}\n\n"
                f"Ключ: {shift}\n\n"
                f"Зашифрованный текст (ШТ):\n{result}\n"
            )
            st.success("Текст зашифрован. Файл готов к скачиванию.")

        else:
            if shift is None:
                all_results = decrypt(user_text, None)
                file_name = "Шифр_Цезаря_Расшифровка_Все_Ключи.txt"
                lines = [
                    "Результат расшифровки (перебор ключей)",
                    f"ШИФР-ТЕКСТ (ШТ):\n{user_text}\n"
                ]
                for k in range(1, 32):
                    lines.append(f"Ключ: {k}")
                    lines.append(f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {all_results[k]}")
                    lines.append("")
                file_content = "\n".join(lines)
                st.info("Расшифровка перебором выполнена. Файл готов к скачиванию.")
            else:
                st.session_state.dec_variants[shift] = decrypt(user_text, shift)

                file_name = "Шифр_Цезаря_Расшифровка.txt"
                lines = [
                    "Результаты расшифровки (выбранные ключи)",
                    f"ШИФР-ТЕКСТ (ШТ):\n{user_text}\n"
                ]
                for k in sorted(st.session_state.dec_variants.keys()):
                    lines.append(f"Ключ: {k}")
                    lines.append(f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {st.session_state.dec_variants[k]}")
                    lines.append("")
                file_content = "\n".join(lines)
                st.success("Вариант добавлен/обновлён. Файл готов к скачиванию.")

        if file_content and file_name:
            st.download_button(
                label="Скачать файл",
                data=file_content,
                file_name=file_name,
                mime="text/plain",
                key="download_btn"
            )
