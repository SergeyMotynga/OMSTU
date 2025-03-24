from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet


class RegressionPipeline:
    def __init__(self, model_scope='multiply', model_type='linear', poly_degree=2, **params):
        self.model_scope = model_scope
        self.model_type = model_type
        self.poly_degree = poly_degree
        self.params = params
        self.pipeline = self._build_pipeline()

    
    @staticmethod
    def _regressor(model_type, **kwargs):
        if model_type == 'linear':
            return LinearRegression(**kwargs)
        elif model_type == 'lasso':
            return Lasso(**kwargs)
        elif model_type == 'ridge':
            return Ridge(**kwargs)
        elif model_type == 'elasticnet':
            return ElasticNet(**kwargs)
        

    def _build_pipeline(self):
        steps = [('scaler', StandardScaler())]
        if self.model_scope == 'polynomial':
            steps.append(('poly', PolynomialFeatures(degree=self.poly_degree, include_bias=False)))
        steps.append(('regressor', RegressionPipeline._regressor(model_type=self.model_type, **self.params)))
        return Pipeline(steps)
    

    def fit(self, X_train, y_train):
        self.pipeline.fit(X_train, y_train)
        return self
    
    def predict(self, X_test):
        return self.pipeline.predict(X_test)
