import os
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import joblib

# Установить рабочую директорию
os.chdir(r'C:\Users\motyn\Desktop\Repositories\OMSTU\Practicum\laboratory\lab_5')

def main():
    os.makedirs('models', exist_ok=True)

    df = pd.read_csv(os.path.join('data', 'train.csv'))
    X = df.drop(columns=['collision'])
    y = df['collision']

    model = GaussianNB()
    model.fit(X, y)

    joblib.dump(model, os.path.join('models', 'naive_bayes.pkl'))
    print("Наивный Байес обучен и сохранён!")

if __name__ == "__main__":
    main()
