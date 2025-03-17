import optuna as pt
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso, Ridge, ElasticNet

def optuna(model_name, X_train, y_train, X_test, y_test):
    def objective(trial):
        alpha = trial.suggest_float("alpha", 1e-5, 1e2)

        if model_name == 'lasso':
            model = Lasso(alpha=alpha)
        elif model_name == 'ridge':
            model = Ridge(alpha=alpha)
        elif model_name == 'elasticnet':
            l1_ratio = trial.suggest_float('l1_ratio', 0.0, 1.0)
            model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return mse
    
    study = pt.create_study(direction="minimize")
    study.optimize(objective, n_trials=100)
    best_parameters = study.best_params
    return best_parameters['alpha'] if model_name != 'elasticnet' else (best_parameters['alpha'], best_parameters['l1_ratio'])
