import streamlit as st

EXCEPTIONS = '.,?!-" '

def isRussia(letter: str) -> bool:
    return 1040 <= ord(letter) <= 1103

def encryption(text: str, k: int) -> str:
    result = ''
    for ch in text:
        if not isRussia(ch) or ch in EXCEPTIONS:
            result += ch
            continue
        if ch.islower():
            result += chr(ord('а') + (ord(ch) + k - ord('а')) % 32)
        else:
            result += chr(ord('А') + (ord(ch) + k - ord('А')) % 32)
    return result

def decrypt_enumeration(text: str):
    result = {}
    for k in range(1, 32):
        out = ''
        for ch in text:
            if not isRussia(ch) or ch in EXCEPTIONS:
                out += ch
                continue
            if ch.islower():
                out += chr(ord('я') - (ord('я') - ord(ch) + k) % 32)
            else:
                out += chr(ord('Я') - (ord('Я') - ord(ch) + k) % 32)
        result[k] = out
    return result

def decrypt(text: str, k: int=None):
    if k is None:
        return decrypt_enumeration(text)
    out = ''
    for ch in text:
        if not isRussia(ch) or ch in EXCEPTIONS:
            out += ch
            continue
        if ch.islower():
            out += chr(ord('я') - (ord('я') - ord(ch) + k) % 32)
        else:
            out += chr(ord('Я') - (ord('Я') - ord(ch) + k) % 32)
    return out

def parse_shift_input(label: str, key: str):
    """
    Возвращает (shift_int_or_None, is_valid, error_message)
    Пустое значение -> None, not valid (если обязательно)
    """
    raw = st.text_input(label, key=key, placeholder="1–31")
    raw = raw.strip()
    if raw == "":
        return None, False, "Укажите ключ от 1 до 31."
    try:
        val = int(raw)
    except ValueError:
        return None, False, "Ключ должен быть целым числом."
    if 1 <= val <= 31:
        return val, True, ""
    return None, False, "Ключ должен быть в диапазоне от 1 до 31."

def get_shift(action: str):
    """
    Возвращает (shift_or_None, is_valid)
    - Для Шифровки ключ обязателен и валидность проверяется.
    - Для Расшифровки: если выбран чекбокс, проверяем валидность; иначе None/valid.
    """
    if action == "Шифровка":
        shift, ok, err = parse_shift_input("Шаг от 1 до 31", "enc_shift")
        if not ok and err:
            st.warning(err)
        return shift, ok
    else:
        use_step = st.checkbox("Указать шаг вручную", value=False, key="dec_use_step")
        if use_step:
            shift, ok, err = parse_shift_input("Шаг от 1 до 31", "dec_shift")
            if not ok and err:
                st.warning(err)
            return shift, ok
        else:
            return None, True

def main_page():
    st.set_page_config(page_title="Шифр Цезаря", page_icon="🔑", layout="centered")
    st.title("Шифр Цезаря")

    st.session_state.setdefault("dec_variants", {})
    st.session_state.setdefault("last_text_for_variants", "")
    st.session_state.setdefault("last_result_title", "")
    st.session_state.setdefault("last_result_text", "")

    user_text = st.text_area("Введите текст:").replace('ё', 'е').replace('Ё', 'Е')

    if user_text != st.session_state.last_text_for_variants:
        st.session_state.dec_variants = {}
        st.session_state.last_text_for_variants = user_text

    action = st.selectbox("Выберите действие:", ("Шифровка", "Расшифровка"))
    shift, shift_valid = get_shift(action)

    if action == "Расшифровка" and shift is not None:
        if st.button("Очистить накопленные варианты", key="clear_variants_btn"):
            st.session_state.dec_variants = {}
            st.info("Список вариантов очищен.")

    disable_action = (user_text.strip() == "") or (not shift_valid)
    do_action = st.button(action, key="do_action_btn", disabled=disable_action, use_container_width=True)

    if do_action:
        file_name = None
        file_content = None

        if action == "Шифровка":
            result = encryption(user_text, shift)
            st.session_state.last_result_title = f"Зашифрованный текст (ШТ), ключ {shift}"
            st.session_state.last_result_text = result

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
                st.session_state.last_result_title = "Перебор ключей (превью)"
                preview_key = st.selectbox("Показать результат для ключа:", list(range(1, 32)), key="preview_key")
                st.session_state.last_result_text = all_results.get(preview_key, "")

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
                dec = decrypt(user_text, shift)
                st.session_state.dec_variants[shift] = dec

                st.session_state.last_result_title = f"Расшифрованный текст (ОТ), ключ {shift}"
                st.session_state.last_result_text = dec

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
                key="download_btn",
                use_container_width=True
            )

    if st.session_state.get("last_result_text", ""):
        st.subheader(st.session_state.get("last_result_title", "Результат"))
        st.text_area(
            "Последний вывод:",
            value=st.session_state["last_result_text"],
            height=200,
            key="last_output_area",
        )