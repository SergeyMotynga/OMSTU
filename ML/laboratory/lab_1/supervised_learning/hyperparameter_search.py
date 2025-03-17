from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def hyperparameter_search(model_name, method_search, parameters, X_train, y_train, max_iter=10000):
    model_name = model_name.lower()
    method_search = method_search.lower()

    if model_name == 'lasso':
        model = Lasso(max_iter=max_iter)
    if model_name == 'ridge':
        model = Ridge(max_iter=max_iter)
    if model_name == 'elasticnet':
        model = ElasticNet(max_iter=max_iter)

    if method_search == 'gridsearchcv':
        search = GridSearchCV(model, parameters, cv=5)
    elif method_search == 'randomizedsearchcv':
        search = RandomizedSearchCV(model, parameters, cv=5)

    search.fit(X_train, y_train)

    return search.best_params_