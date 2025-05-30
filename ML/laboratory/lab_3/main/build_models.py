from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, GradientBoostingClassifier, StackingClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def build_models(
        max_iter: int=10000,
        random_state: int=42,
        model_name=None
        ):
    dt = DecisionTreeClassifier(random_state=random_state)
    lg = LogisticRegression(max_iter=max_iter, random_state=random_state)
    knn = KNeighborsClassifier()
    nb = GaussianNB()
    cb = CatBoostClassifier()
    xgb = XGBClassifier()
    lb = LGBMClassifier()
    svm = SVC(probability=True, random_state=random_state)
    rf = RandomForestClassifier(random_state=random_state, n_jobs=2)
    base_estimators = [
        ('dt',  dt),
        ('knn', knn)
    ]

    models = {
        'StackingClassifier'.lower(): StackingClassifier(estimators=base_estimators, final_estimator=lg, n_jobs=2),
        'GradientBoostingClassifier'.lower(): GradientBoostingClassifier(random_state=random_state),
        'BaggingClassifier'.lower(): BaggingClassifier(n_jobs=2, random_state=random_state),
        'RandomForestClassifier'.lower(): rf,
        'DecisionTreeClassifier'.lower(): dt,
        'LogisticRegression'.lower(): lg,
        'kNN'.lower(): knn,
        'NaiveBayes'.lower(): nb,
        'SVM'.lower(): svm,
        'CatBoostClassifier'.lower(): cb,
        'XGBClassifier'.lower(): xgb,
        'LGBMClassifier'.lower(): lb
        }
    return models[model_name]