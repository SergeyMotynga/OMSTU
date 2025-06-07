import joblib
model_path = r"ML\laboratory\lab_3\main\models\classifier\gb_classifier_model"
model = joblib.load(model_path)
print("Модель загружена успешно")