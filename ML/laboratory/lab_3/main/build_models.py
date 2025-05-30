from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, GradientBoostingClassifier, StackingClassifier, RandomForestRegressor, BaggingRegressor, GradientBoostingRegressor, StackingRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor

def build_models(
        max_iter: int=10000,
        random_state: int=42,
        model_name=None
        ):
    dt_r = DecisionTreeRegressor(random_state=random_state)
    rf_r = RandomForestRegressor(random_state=random_state, n_jobs=2)
    cb_r = CatBoostRegressor()
    xgb_r = XGBRegressor()
    lb_r = LGBMRegressor()
    dt_cl = DecisionTreeClassifier(random_state=random_state)
    lg = LogisticRegression(max_iter=max_iter, random_state=random_state)
    knn_cl = KNeighborsClassifier()
    knn_r = KNeighborsRegressor()
    nb = GaussianNB()
    cb_cl = CatBoostClassifier()
    xgb_cl = XGBClassifier()
    lb_cl = LGBMClassifier()
    svc = SVC(probability=True, random_state=random_state)
    rf_cl = RandomForestClassifier(random_state=random_state, n_jobs=2)
    base_estimators_cl = [
        ('dt',  dt_cl),
        ('knn', knn_cl)
    ]
    base_estimators_r = [
        ('dt',  dt_r),
        ('knn', knn_r)
    ]

    models = {
        'StackingClassifier'.lower(): StackingClassifier(estimators=base_estimators_cl, final_estimator=lg, n_jobs=2),
        'GradientBoostingClassifier'.lower(): GradientBoostingClassifier(random_state=random_state),
        'BaggingClassifier'.lower(): BaggingClassifier(n_jobs=2, random_state=random_state),
        'StackingRegressor'.lower(): StackingRegressor(estimators=base_estimators_r, final_estimator=SVR(), n_jobs=2),
        'GradientBoostingRegressor'.lower(): GradientBoostingRegressor(random_state=random_state),
        'BaggingRegressor'.lower(): BaggingRegressor(n_jobs=2, random_state=random_state),
        'RandomForestClassifier'.lower(): rf_cl,
        'RandomForestRegressor'.lower(): rf_r,
        'DecisionTreeClassifier'.lower(): dt_cl,
        'DecisionTreeRegressor'.lower(): dt_r,
        'LogisticRegression'.lower(): lg,
        'kNN'.lower(): knn_cl,
        'NaiveBayes'.lower(): nb,
        'SVC'.lower(): svc,
        'CatBoostClassifier'.lower(): cb_cl,
        'XGBClassifier'.lower(): xgb_cl,
        'LGBMClassifier'.lower(): lb_cl,
        'CatBoostRegressor'.lower(): cb_r,
        'XGBRegressor'.lower(): xgb_r,
        'LGBMRegressor'.lower(): lb_r
        }
    return models[model_name]