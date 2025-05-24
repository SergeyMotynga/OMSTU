import os
import csv
from predict_logreg import predict_logreg
from predict_nb import predict_nb
from predict_svm import predict_svm

def run_all_predictions():
    results = []
    for model_name, predict_func in [
        ("LogisticRegression", predict_logreg),
        ("NaiveBayes", predict_nb),
        ("SVM", predict_svm)
    ]:
        try:
            result = predict_func()
            if result:
                results.append(result)
        except Exception as e:
            print(f"Error in {model_name}: {e}")

    csv_path = os.path.join("data", "model_results.csv")
    with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["model", "accuracy", "precision", "recall", "time_ms"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    run_all_predictions()
