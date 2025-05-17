from scipy.stats import randint, uniform

parameters = {
    'DecisionTreeClassifier': {
        'GridSearchCV': {
            'criterion':          ['gini', 'entropy'],
            'max_depth':          [5, 10, None],
            'min_samples_leaf':   [1, 5, 10],
            'class_weight':       [None, 'balanced']
        },
        'RandomizedSearchCV': {
            'criterion':           ['gini', 'entropy', 'log_loss'],
            'splitter':            ['best', 'random'],
            'max_depth':           randint(3, 30),
            'min_samples_split':   randint(2, 50),
            'min_samples_leaf':    randint(1, 20),
            'max_features':        [None, 'sqrt', 'log2', 0.3, 0.5, 0.7],
            'max_leaf_nodes':      randint(10, 100),
            'ccp_alpha':           uniform(0.0, 0.02),
            'class_weight':        [None, 'balanced', {0:1,1:3}, {0:1,1:5}]
        }
    },
    'RandomForestClassifier': {
        'GridSearchCV': {
            'n_estimators':       [100, 200, 500],
            'criterion':          ['gini', 'entropy'],
            'max_depth':          [None, 10, 20, 30],
            'min_samples_split':  [2, 5, 10],
            'min_samples_leaf':   [1, 2, 4],
            'max_features':       ['sqrt', 'log2', None],
            'bootstrap':          [True, False]
        },
        'RandomizedSearchCV': {
            'n_estimators':       randint(50, 500),
            'criterion':          ['gini', 'entropy'],
            'max_depth':          randint(5, 50),
            'min_samples_split':  randint(2, 20),
            'min_samples_leaf':   randint(1, 20),
            'max_features':       uniform(0.1, 0.9),
            'bootstrap':          [True],
            'oob_score':          [True, False],
            'ccp_alpha':          uniform(0.0, 0.02)
        }
    },
    'BaggingClassifier': {
        'GridSearchCV': {
            'n_estimators':      [10, 50, 100],
            'max_samples':       [0.5, 1.0],
            'max_features':      [0.5, 1.0],
            'bootstrap':         [True, False]
        },
        'RandomizedSearchCV': {
            'n_estimators':      randint(10, 100),
            'max_samples':       uniform(0.5, 0.5),
            'max_features':      uniform(0.5, 0.5),
            'bootstrap':         [True, False]
        }
    },
    'GradientBoostingClassifier': {
        'GridSearchCV': {
            'n_estimators':      [50, 100, 150],
            'learning_rate':     [0.01, 0.1, 0.2],
            'subsample':         [0.6, 0.8, 1.0],
            'max_depth':         [3, 5, 7],
            'max_features':      ['sqrt', 'log2', None]
        },
        'RandomizedSearchCV': {
            'n_estimators':      randint(50, 200),
            'learning_rate':     uniform(0.01, 0.19),
            'subsample':         uniform(0.6, 0.4),
            'max_depth':         randint(2, 8),
            'min_samples_leaf':  randint(1, 10),
            'max_features':      ['sqrt', 'log2', None]
        }
    },
    'StackingClassifier': {
        'GridSearchCV': {
            'passthrough':             [True, False],
            'final_estimator__C':      [0.1, 1.0, 10.0]
        },
        'RandomizedSearchCV': {
            'passthrough':             [True, False],
            'final_estimator__C':      uniform(0.01, 9.99)
        }
    },
    'CatBoostClassifier': {
        'GridSearchCV': {
            'iterations':      [100, 200, 500],
            'depth':           [4, 6, 8],
            'learning_rate':   [0.01, 0.1, 0.2],
            'l2_leaf_reg':     [3, 5, 7],
            'rsm':             [0.6, 0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'iterations':        randint(50, 500),
            'depth':             randint(3, 10),
            'learning_rate':     uniform(0.01, 0.19),
            'l2_leaf_reg':       randint(1, 10),
            'rsm':               uniform(0.5, 0.5),
            'bagging_temperature': uniform(0.0, 1.0)
        }
    },
    'XGBClassifier': {
        'GridSearchCV': {
            'n_estimators':      [100, 200, 500],
            'max_depth':         [3, 6, 9],
            'learning_rate':     [0.01, 0.1, 0.2],
            'subsample':         [0.6, 0.8, 1.0],
            'colsample_bytree':  [0.6, 0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':      randint(50, 500),
            'max_depth':         randint(3, 12),
            'learning_rate':     uniform(0.01, 0.19),
            'subsample':         uniform(0.5, 0.5),
            'colsample_bytree':  uniform(0.5, 0.5),
            'reg_alpha':         uniform(0.0, 1.0),
            'reg_lambda':        uniform(0.0, 1.0)
        }
    },
    'LGBMClassifier': {
        'GridSearchCV': {
            'n_estimators':      [100, 200, 500],
            'learning_rate':     [0.01, 0.1, 0.2],
            'num_leaves':        [31, 50, 100],
            'subsample':         [0.6, 0.8, 1.0],
            'colsample_bytree':  [0.6, 0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':      randint(50, 500),
            'learning_rate':     uniform(0.01, 0.19),
            'num_leaves':        randint(20, 150),
            'subsample':         uniform(0.5, 0.5),
            'colsample_bytree':  uniform(0.5, 0.5),
            'reg_alpha':         uniform(0.0, 1.0),
            'reg_lambda':        uniform(0.0, 1.0)
        }
    }
}
