import os
import pandas as pd
import joblib
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score

os.chdir(r'C:\Users\motyn\Desktop\Repositories\OMSTU\Practicum\laboratory\lab_5')

def predict_nb():
    start = time.time()
    model = joblib.load(os.path.join('models', 'naive_bayes.pkl'))
    df = pd.read_csv(os.path.join('data', 'new_data.csv'))

    X = df.drop(columns=["collision"])
    y_true = df["collision"]
    y_pred = model.predict(X)
    stop = round((time.time() - start) * 1000, 2)

    result = {
        "model": "NaiveBayes",
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "time_ms": stop
    }
    return result


if __name__ == "__main__":
    predict_nb()