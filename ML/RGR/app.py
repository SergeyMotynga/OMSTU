import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
import numpy as np
import tensorflow as tf

# Настройка страницы Streamlit
st.set_page_config(page_title="ML Дашборд", layout="wide")

# Определение страниц приложения
def developer_info():
    # Страница с информацией о разработчике
    st.title("Информация о разработчике")
    st.header("О разработчике")
    st.write("**ФИО**: Мотынга Сергей Андреевич")  # Замени на свои данные
    st.write("**Номер группы**: ФИТ-231")  # Замени на свой номер группы
    st.write("**Тема РГР**: Разработка Web-приложения (дашборда) для инференса моделей ML и анализа данных")
    
    # Отображение фотографии разработчика
    try:
        image = Image.open("developer_photo.jpg")  # Укажи путь к своей фотографии
        st.image(image, caption="Фото разработчика", width=300)
    except FileNotFoundError:
        st.warning("Фото разработчика не найдено. Загрузи файл 'developer_photo.jpg'.")

def dataset_info():
    # Страница с описанием датасета
    st.title("Информация о датасете")
    st.header("Описание датасета")
    st.write("""
    **Название датасета**: csgo.csv  \n
    **Предметная область**: Прогнозирование, будет ли поставлена бомба в конкретном раунде в игре SC:GO\n
    **Описание**: Этот датасет содержит всю информацию об обоих командах в раунде.\n
    **Признаки**:  
    - time_left: Оставшееся время до конца раунда (численный, секунды) 
    - ct_score: Количество раундов, которое сторона защиты выйграла к текущему раунду (численный) 
    - t_score: Количество раундов, которое сторона атаки выйграла к текущему раунду (численный) 
    - map: Название карты, на которой происходит игра (категориальный)
    - ct_health: Суммарное количество здоровья у стороны защиты (численный)
    - t_health: Суммарное количество здоровья у стороны атаки (численный)
    - ct_armor: Суммарное количество брони у стороны защиты (численный)
    - t_armor: Суммарное количество брони у стороны атаки (численный)
    - ct_money: Суммарное количество денег у стороны защиты (численный)
    - t_money: Суммарное количество денег у стороны атаки (численный)
    - ct_helmets: Суммарное количество шлемов у стороны защиты (численный)
    - t_helmets: Суммарное количество шлемов у стороны атаки (численный)
    - ct_defuse_kits: Суммарное количество снаряжения для разминирования бомбы у стороны защиты (численный)
    - ct_players_alive: Суммарное количество игроков, которые живы у стороны защиты (численный)
    - t_players_alive: Суммарное количество игроков, которые живы у стороны атаки (численный)\n
    **Целевая переменная**: bomb_planted: Информация о том, была ли поставлена бомба в раунде (бинарный True/False)\n
    **Предобработка**:  
    - Обработка пропущенных значений: заполнены средним по группировкам.
    - Масштабирование числовых признаков: StandardScaler.\n
    **EDA**: Проведён исследовательский анализ данных для выявления корреляций, выбросов и распределений признаков.
    """)

def visualizations():
    # Страница с визуализациями данных
    st.title("Визуализации данных")
    st.header("Исследовательский анализ данных")
    
    # Загрузка датасета (замени на свой путь к файлу)
    try:
        df = pd.read_csv("csgo_filtred.csv")  # Укажи путь к своему датасету
    except FileNotFoundError:
        st.error("Файл датасета 'your_dataset.csv' не найден. Загрузи правильный файл.")
        return
    
    # Удаление ненужных столбцов
    columns_to_drop = ['health_lead', 'armor_lead', 'money_lead', 'helmets_lead', 'players_alive_lead']
    # Проверяем, какие из указанных столбцов существуют в датасете
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    
    # Определение числовых признаков
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    target_col = 'bomb_planted'
    
    # Удаляем целевую переменную из списка числовых признаков, если она числовая
    if target_col in numeric_cols:
        numeric_cols.remove(target_col)
    
    # Визуализация 1: Гистограммы всех числовых признаков на одном графике
    st.subheader("Гистограммы всех числовых признаков")
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3  # Определяем количество строк для 3 столбца в ряду
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows), constrained_layout=True)
    axes = axes.flatten()  # Преобразуем массив осей в одномерный для удобства
    for i, col in enumerate(numeric_cols):
        sns.histplot(df[col], bins=30, kde=True, ax=axes[i], log=True)
        axes[i].set_title(f"Распределение {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Количество")
    # Скрываем пустые подграфики, если их больше, чем признаков
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    st.pyplot(fig)
    
    # Визуализация 2: Скрипичные графики всех числовых признаков по целевой переменной на одном графике
    st.subheader("Скрипичные графики всех числовых признаков по целевой переменной")
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows), constrained_layout=True)
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.violinplot(x=target_col, y=col, data=df, ax=axes[i])
        axes[i].set_title(f"{col} по {target_col}")
        axes[i].set_xlabel(target_col)
        axes[i].set_ylabel(col)
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    st.pyplot(fig)
    
    # Визуализация 3: Тепловая карта корреляций
    st.subheader("Тепловая карта корреляций")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Корреляции числовых признаков")
    st.pyplot(fig)


def prediction():
    # Страница для предсказаний
    st.title("Предсказания модели")
    st.header("Получение предсказаний от моделей ML")
    
    # Список всех доступных моделей
    model_names = [
        "DecisionTree",
        "GradientBoost",
        "CatBoost",
        "Bagging",
        "Stacking",
        "NerualNetwork"
    ]
    
    # Пути к сохранённым моделям
    model_paths = {
        "DecisionTree": "models/dt_classifier_model",
        "GradientBoost": "models/gb_classifier_model",
        "CatBoost": "models/cb_classifier_model",
        "Bagging": "models/bc_classifier_model",
        "Stacking": "models/st_classifier_model",
        "NerualNetwork": "models/nn_model_classification.h5"
    }
    
    # Ожидаемые признаки (определены до всех блоков)
    expected_features = [
        'time_left', 'ct_score', 't_score', 'map', 'ct_health', 't_health',
        'ct_armor', 't_armor', 'ct_money', 't_money', 'ct_helmets', 't_helmets',
        'ct_defuse_kits', 'ct_players_alive', 't_players_alive'
    ]
    
    # Выбор моделей с помощью мультиселекта
    selected_models = st.multiselect(
        "Выберите модели для предсказания",
        model_names,
        default=model_names[:6]
    )

    # Словарь для преобразования карты
    mapping = {
        'de_inferno': 1,
        'de_dust2': 2,
        'de_nuke': 3,
        'de_mirage': 4,
        'de_overpass': 5,
        'de_train': 6,
        'de_vertigo': 7,
        'unknown': 8,
        'de_cache': 9
    }
    
    # Функция для вычисления дополнительных признаков
    def compute_lead_features(data):
        data['health_lead'] = np.where(data['ct_health'] > data['t_health'], 0, 
                                       np.where(data['t_health'] > data['ct_health'], 1, 2))
        data['armor_lead'] = np.where(data['ct_armor'] > data['t_armor'], 0, 
                                      np.where(data['t_armor'] > data['ct_armor'], 1, 2))
        data['money_lead'] = np.where(data['ct_money'] > data['t_money'], 0, 
                                      np.where(data['t_money'] > data['ct_money'], 1, 2))
        data['helmets_lead'] = np.where(data['ct_helmets'] > data['t_helmets'], 0, 
                                        np.where(data['t_helmets'] > data['ct_helmets'], 1, 2))
        data['players_alive_lead'] = np.where(data['ct_players_alive'] > data['t_players_alive'], 0, 
                                              np.where(data['t_players_alive'] > data['ct_players_alive'], 1, 2))
        return data
    
    # Загрузка файла CSV
    st.subheader("Загрузите данные для предсказания")
    uploaded_file = st.file_uploader("Загрузите CSV-файл", type=["csv"])
    
    if uploaded_file:
        try:
            input_data = pd.read_csv(uploaded_file)
            st.write("Предпросмотр загруженных данных:")
            st.dataframe(input_data.head())
            
            # Преобразование столбца map
            if 'map' in input_data.columns:
                input_data['map'] = input_data['map'].str.strip().str.lower().map(mapping)
                if input_data['map'].isna().any():
                    st.error("Некоторые значения в столбце 'map' не соответствуют допустимым картам.")
                    return
            
            # Валидация входных данных
            if set(input_data.columns) >= set(expected_features):
                # Вычисление дополнительных признаков
                input_data = compute_lead_features(input_data)
                
                # Выборка всех необходимых признаков
                all_features = expected_features + ['health_lead', 'armor_lead', 'money_lead', 'helmets_lead', 'players_alive_lead']
                input_data = input_data[all_features]
                
                st.subheader("Результаты предсказания")
                results = []
                for model_name in selected_models:
                    model_path = model_paths.get(model_name)
                    if os.path.exists(model_path):
                        try:
                            if model_name == "NerualNetwork":
                                model = tf.keras.models.load_model(model_path)
                                predictions = np.argmax(model.predict(input_data), axis=1)
                            else:
                                model = joblib.load(model_path)
                                predictions = model.predict(input_data)
                            results.append({
                                "Модель": model_name,
                                "Предсказания": ["Бомба поставлена" if pred == 1 else "Бомба не поставлена" for pred in predictions]
                            })
                        except Exception as e:
                            st.error(f"Ошибка загрузки модели {model_name}: {e}")
                    else:
                        st.error(f"Файл модели {model_path} не найден.")
                
                # Вывод результатов в таблице
                if results:
                    results_df = pd.DataFrame({r["Модель"]: r["Предсказания"] for r in results})
                    st.dataframe(results_df)
            else:
                st.error(f"Загруженный CSV не содержит все ожидаемые признаки: {expected_features}")
        except Exception as e:
            st.error(f"Ошибка обработки файла: {e}")
    
    # Форма для ручного ввода данных
    st.subheader("Или введите данные вручную")
    with st.form("input_form"):
        time_left = st.slider("Оставшееся время до конца раунда (секунды)", min_value=0.1, max_value=175.0, step=0.1)
        ct_score = st.slider("Количество раундов, выигранных стороной защиты", min_value=0, max_value=15, step=1)
        t_score = st.slider("Количество раундов, выигранных стороной атаки", min_value=0, max_value=15, step=1)
        map_value = st.selectbox("Карта", list(mapping.keys()))
        ct_health = st.slider("Суммарное здоровье стороны защиты", min_value=0, max_value=500, step=1)
        t_health = st.slider("Суммарное здоровье стороны атаки", min_value=0, max_value=500, step=1)
        ct_armor = st.slider("Суммарная броня стороны защиты", min_value=0, max_value=500, step=1)
        t_armor = st.slider("Суммарная броня стороны атаки", min_value=0, max_value=500, step=1)
        ct_money = st.slider("Суммарное количество денег стороны защиты", min_value=0, max_value=80000, step=100)
        t_money = st.slider("Суммарное количество денег стороны атаки", min_value=0, max_value=80000, step=100)
        ct_helmets = st.slider("Суммарное количество шлемов стороны защиты", min_value=0, max_value=5, step=1)
        t_helmets = st.slider("Суммарное количество шлемов стороны атаки", min_value=0, max_value=5, step=1)
        ct_defuse_kits = st.slider("Суммарное количество наборов для разминирования", min_value=0, max_value=5, step=1)
        ct_players_alive = st.slider("Количество живых игроков стороны защиты", min_value=0, max_value=5, step=1)
        t_players_alive = st.slider("Количество живых игроков стороны атаки", min_value=0, max_value=5, step=1)
        submit = st.form_submit_button("Предсказать")
        
        if submit:
            # Подготовка входных данных
            input_data = pd.DataFrame({
                'time_left': [time_left],
                'ct_score': [ct_score],
                't_score': [t_score],
                'map': [mapping[map_value]],  # Преобразование карты в число
                'ct_health': [ct_health],
                't_health': [t_health],
                'ct_armor': [ct_armor],
                't_armor': [t_armor],
                'ct_money': [ct_money],
                't_money': [t_money],
                'ct_helmets': [ct_helmets],
                't_helmets': [t_helmets],
                'ct_defuse_kits': [ct_defuse_kits],
                'ct_players_alive': [ct_players_alive],
                't_players_alive': [t_players_alive]
            })
            
            # Вычисление дополнительных признаков
            input_data = compute_lead_features(input_data)
            
            # Выборка всех необходимых признаков
            all_features = expected_features + ['health_lead', 'armor_lead', 'money_lead', 'helmets_lead', 'players_alive_lead']
            input_data = input_data[all_features]
            
            # Выполнение предсказания
            st.subheader("Результат предсказания")
            results = []
            for model_name in selected_models:
                model_path = model_paths.get(model_name)
                if os.path.exists(model_path):
                    try:
                        if model_name == "NerualNetwork":
                            model = tf.keras.models.load_model(model_path)
                            predictions = np.argmax(model.predict(input_data), axis=1)
                        else:
                            model = joblib.load(model_path)
                            predictions = model.predict(input_data)
                        results.append({
                            "Модель": model_name,
                            "Предсказания": ["Бомба поставлена" if pred == 1 else "Бомба не поставлена" for pred in predictions]
                        })
                    except Exception as e:
                        st.error(f"Ошибка загрузки модели {model_name}: {e}")
                else:
                    st.error(f"Файл модели {model_path} не найден.")
            
            # Вывод результатов в таблице
            if results:
                results_df = pd.DataFrame(results)
                st.dataframe(results_df)

# Настройка навигации
pages = {
    "Информация о разработчике": developer_info,
    "Информация о датасете": dataset_info,
    "Визуализации": visualizations,
    "Предсказания": prediction
}

st.sidebar.title("Навигация")
selection = st.sidebar.radio("Перейти к", list(pages.keys()))
page = pages[selection]
page()
