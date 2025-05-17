from typing import Literal, Dict, Any, Optional
from build_models import build_models
from build_method_search import build_method_search
from build_pipeline import build_pipeline


def search_hyperparameters(
        model_name: Literal['LogisticRegression', 'kNN', 'NaiveBayes', 'SVM', 'DecisionTreeClassifier']=None,
        method_search: Literal['GridSearchCV', 'RandomizedSearchCV']=None,
        X_train=None,
        y_train=None,
        param_grid: Dict[str, Any]=None,
        max_iter: int=10000,
        cv: int=5,
        random_state: int=42,
        n_iter: int=30,
        n_jobs: int=2,
        scoring: Optional[str]=None,
        balanced: bool=True
        ) -> dict:
    '''
    search_hyperparameters - функция для поиска гиперпараметров для основных моделей классификации обучения с учитеелем (find bests hyperparameters for most popular classifier models on supervised learning)

    Parameters
    ----------
    model_name : {'LogisticRegression', 'kNN', 'NaiveBayes', 'SVM'}, default=None
        Название модели классификации (name of classifier model)

    method_search : {'GridSearchCV', 'RandomizedSearchCV'}, default=None
        Название метода для поиска гиперпараметров (name of method for search hyperparameters)\n

    X_train : MatrixLike | ArrayLike, default=None
        Тренировочная матрица | массив признаков (train features matrix | array)

    y_train : ArrayLike, default=None
        Тренировочный массив целевого признака (train target array)

    param_grid : Dict, default=None
        Словарь гиперпараметров соответствующих для модели классификации (dictionary of hyperparameters for classifier model)

    max_iter : int, default=10000
        Число максимального количества итераций для модели классификации (number of max number iteration for classifier model)

    cv : int, default=5
        Количество фолдов для кросс-валидации (number of folds for cross-validation)

    random_state : int, default=42
        Базовое значение для генератора случайных чисел (base number for generate random numbers (seed))

    n_iter : int, default=30
        Число примеров для метода RandomizedSearchCV (number sampled in RandomizedSearchCV)

    n_jobs : int, default=2
        Количество одновременно выполняемых потоков (number of threads running simultaneously)
        - `-1` : использование всех потоков (used all threads)
        - `1` : использование только одного потока (no parallelism)
        - `>1` : количество используемых потоков (number of threads running)

    scoring : Optional[str], default=None
        Метрика оценки модели классификации (metric for evaluation classifier model)
    '''
    model_name = model_name.lower()
    method_search = method_search.lower()
    model = build_models(max_iter=max_iter, random_state=random_state, model_name=model_name)
    if balanced:
        model = build_pipeline(model)
        param_grid = {f"model__{k}": v for k, v in param_grid.items()} 
    search = build_method_search(method_search=method_search, model=model, cv=cv, param_grid=param_grid, scoring=scoring, n_jobs=n_jobs, n_iter=n_iter)
        
    search.fit(X_train, y_train)
    return {
        'best_params': search.best_params_,
        'best_score': search.best_score_
    }