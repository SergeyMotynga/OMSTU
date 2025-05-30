from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline(model, scaler: bool=True, sample=True, sampler='undersample', sampling_strategy=0.3):
    steps = []

    if scaler:
        steps.append(('scaler', StandardScaler()))
    
    if sample:
        if sampler == 'combine':
            steps.append(('sampler', SMOTEENN(sampling_strategy=sampling_strategy, random_state=42)))
        elif sampler == 'undersample':
            steps.append(('sampler', RandomUnderSampler(sampling_strategy=0.3, random_state=42)))
        else:
            steps.append(('sampler', SMOTE(sampling_strategy=0.3, random_state=42)))

    steps.append(('model', model))
    return Pipeline(steps)