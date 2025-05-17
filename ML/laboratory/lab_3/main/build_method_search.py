from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


def build_method_search(
        method_search=None,
        model=None,
        cv=None,
        param_grid=None,
        scoring=None,
        n_jobs=None,
        n_iter=None
        ):
    search = None
    if method_search == 'GridSearchCV'.lower():
        search = GridSearchCV(
            estimator=model, 
            param_grid=param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs
            )
    elif method_search == 'RandomizedSearchCV'.lower():
        search = RandomizedSearchCV(
            estimator=model, 
            param_distributions=param_grid,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs
            )
        
    return search