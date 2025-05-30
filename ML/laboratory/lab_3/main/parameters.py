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
            'iterations':      [100, 300],
            'depth':           [4, 8],
            'learning_rate':   [0.05, 0.1],
            'l2_leaf_reg':     [3, 7]
        },
        'RandomizedSearchCV': {
            'iterations':      randint(50, 300),
            'depth':           randint(4, 8),
            'learning_rate':   uniform(0.05, 0.15),
            'l2_leaf_reg':     randint(3, 7)
        }
    },
    'XGBClassifier': {
        'GridSearchCV': {
            'n_estimators':    [100, 300],
            'max_depth':       [3, 6],
            'learning_rate':   [0.05, 0.1],
            'subsample':       [0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':    randint(50, 300),
            'max_depth':       randint(3, 7),
            'learning_rate':   uniform(0.05, 0.15),
            'subsample':       uniform(0.7, 0.3),
            'colsample_bytree': uniform(0.7, 0.3)
        }
    },
    'LGBMClassifier': {
        'GridSearchCV': {
            'n_estimators':    [100, 300],
            'learning_rate':   [0.05, 0.1],
            'num_leaves':      [31, 70],
            'subsample':       [0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':    randint(50, 300),
            'learning_rate':   uniform(0.05, 0.15),
            'num_leaves':      randint(20, 70),
            'subsample':       uniform(0.7, 0.3),
            'colsample_bytree': uniform(0.7, 0.3)
        }
    },
    'DecisionTreeRegressor': {
        'GridSearchCV': {
            'criterion':          ['squared_error', 'absolute_error'],
            'max_depth':          [5, 10, None],
            'min_samples_leaf':   [1, 5, 10],
            'min_samples_split':  [2, 5, 10]
        },
        'RandomizedSearchCV': {
            'criterion':           ['squared_error', 'absolute_error', 'friedman_mse'],
            'splitter':            ['best', 'random'],
            'max_depth':           randint(3, 30),
            'min_samples_split':   randint(2, 50),
            'min_samples_leaf':    randint(1, 20),
            'max_features':        [None, 'sqrt', 'log2', 0.3, 0.5, 0.7],
            'max_leaf_nodes':      randint(10, 100),
            'ccp_alpha':           uniform(0.0, 0.02)
        }
    },
    'RandomForestRegressor': {
        'GridSearchCV': {
            'n_estimators':       [100, 200, 500],
            'criterion':          ['squared_error', 'absolute_error'],
            'max_depth':          [None, 10, 20, 30],
            'min_samples_split':  [2, 5, 10],
            'min_samples_leaf':   [1, 2, 4],
            'max_features':       ['sqrt', 'log2', None],
            'bootstrap':          [True, False]
        },
        'RandomizedSearchCV': {
            'n_estimators':       randint(50, 500),
            'criterion':          ['squared_error', 'absolute_error'],
            'max_depth':          randint(5, 50),
            'min_samples_split':  randint(2, 20),
            'min_samples_leaf':   randint(1, 20),
            'max_features':       uniform(0.1, 0.9),
            'bootstrap':          [True],
            'oob_score':          [True, False],
            'ccp_alpha':          uniform(0.0, 0.02)
        }
    },
    'BaggingRegressor': {
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
    'GradientBoostingRegressor': {
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
    'StackingRegressor': {
        'GridSearchCV': {
            'passthrough':             [True, False],
            'final_estimator__C':      [0.1, 1.0, 10.0]
        },
        'RandomizedSearchCV': {
            'passthrough':             [True, False],
            'final_estimator__C':      uniform(0.01, 9.99)
        }
    },
    'CatBoostRegressor': {
        'GridSearchCV': {
            'iterations':      [100, 300],
            'depth':           [4, 8],
            'learning_rate':   [0.05, 0.1],
            'l2_leaf_reg':     [3, 7]
        },
        'RandomizedSearchCV': {
            'iterations':      randint(50, 300),
            'depth':           randint(4, 8),
            'learning_rate':   uniform(0.05, 0.15),
            'l2_leaf_reg':     randint(3, 7)
        }
    },
    'XGBRegressor': {
        'GridSearchCV': {
            'n_estimators':    [100, 300],
            'max_depth':       [3, 6],
            'learning_rate':   [0.05, 0.1],
            'subsample':       [0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':    randint(50, 300),
            'max_depth':       randint(3, 7),
            'learning_rate':   uniform(0.05, 0.15),
            'subsample':       uniform(0.7, 0.3),
            'colsample_bytree': uniform(0.7, 0.3)
        }
    },
    'LGBMRegressor': {
        'GridSearchCV': {
            'n_estimators':    [100, 300],
            'learning_rate':   [0.05, 0.1],
            'num_leaves':      [31, 70],
            'subsample':       [0.8, 1.0]
        },
        'RandomizedSearchCV': {
            'n_estimators':    randint(50, 300),
            'learning_rate':   uniform(0.05, 0.15),
            'num_leaves':      randint(20, 70),
            'subsample':       uniform(0.7, 0.3),
            'colsample_bytree': uniform(0.7, 0.3)
        }
    }
}