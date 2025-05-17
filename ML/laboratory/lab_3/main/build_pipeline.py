from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from imblearn.combine import SMOTEENN



def build_pipeline(model):
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('sampler', SMOTEENN(sampling_strategy=1, random_state=42)),
        ('model', model)
    ])
    return pipe