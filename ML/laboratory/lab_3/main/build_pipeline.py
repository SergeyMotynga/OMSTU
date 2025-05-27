from imblearn.combine import SMOTEENN
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline(model):
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('sampler', SMOTEENN(sampling_strategy=1, random_state=42)),
        ('model', model)
    ])
    return pipe