<<<<<<< HEAD
from imblearn.combine import SMOTEENN
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
=======
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from imblearn.combine import SMOTEENN

>>>>>>> d6be06d4783f7af6b384982fb6ee5b517da6921c


def build_pipeline(model):
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('sampler', SMOTEENN(sampling_strategy=1, random_state=42)),
        ('model', model)
    ])
    return pipe