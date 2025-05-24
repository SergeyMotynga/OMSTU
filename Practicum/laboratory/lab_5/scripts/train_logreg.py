import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

os.chdir(r'C:\Users\motyn\Desktop\Repositories\OMSTU\Practicum\laboratory\lab_5')

def main():
    os.makedirs('models', exist_ok=True)

    df = pd.read_csv(os.path.join('data', 'train.csv'))
    X = df.drop(columns=['collision'])
    y = df['collision']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    joblib.dump(model, os.path.join('models', 'logistic_regression.pkl'))
    print("Логистическая регрессия обучена и сохранена!")

if __name__ == "__main__":
    main()
