import pandas as pd
from sklearn.svm import SVC
import joblib
import os

os.chdir(r'C:\Users\motyn\Desktop\Repositories\OMSTU\Practicum\laboratory\lab_5')

def main():
    os.makedirs('models', exist_ok=True)

    train_csv_path = os.path.join('data', 'train.csv')
    model_path = os.path.join('models', 'svm.pkl')

    df = pd.read_csv(train_csv_path)
    X = df.drop(columns=['collision'])
    y = df['collision']

    model = SVC(probability=True)
    model.fit(X, y)

    joblib.dump(model, model_path)
    print(f"SVM обучена и сохранена в {model_path}!")

if __name__ == "__main__":
    main()
