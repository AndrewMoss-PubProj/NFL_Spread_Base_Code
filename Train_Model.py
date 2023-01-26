import time
import datetime
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import json
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import timer
import pickle
from sklearn import model_selection
from sklearn.model_selection import KFold

def design_experiment(test, metadata):
    performance = pd.DataFrame(columns=['margin_required','picks_in_set',
                                        'percent_correct', 'money_won'])
    for i in np.linspace(.5, 20, 40):
        if i == 4:
            print()
        best_picks = test.loc[np.where(abs(test['preds'] - test['spread_line']) >= i)[0],:]
        percent_correct = np.mean(best_picks['itm'])
        money_won = np.sum(best_picks['money_gained'])
        # streaks = test['money_gained'].ne(test['money_gained'].shift())
        performance = performance.append({'margin_required': i, 'picks_in_set': len(best_picks),
                                          'percent_correct': percent_correct,
                                          'money_won': money_won}, ignore_index=True)
    best_strat = performance[performance['money_won'] == max(performance['money_won'])]
    metadata['most_money_earned'] = best_strat['money_won'].values[0]
    metadata['best_straregy_pct_correct'] = best_strat['percent_correct'].values[0]
    metadata['sample_size_three_year'] = best_strat['picks_in_set'].values[0]
    metadata['model_confidence_thresh'] = best_strat['margin_required'].values[0]

    json_object = json.dumps(metadata, indent=4)

    # Writing to sample.json
    with open('metadata/' +str(time.time()) + '.json', "w") as outfile:
        outfile.write(json_object)
def train_model():
    data = pd.read_csv('feature_frame.csv')
    train = data[~np.isin(data['season'], [2015, 2016, 2017])]
    test = data[np.isin(data['season'], [2015, 2016, 2017])]
    metadata = {}



    train_inputs = train[['away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
    train_outputs = train['result']
    test_inputs = test[['away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
    test_outputs = test['result']
    print()
    model_kfold_XGB = XGBRegressor()
    kfold = KFold(n_splits=5)

    results_kfold_XGB = model_selection.cross_val_score(model_kfold_XGB, train_inputs, train_outputs,
                                                    scoring='neg_mean_squared_error', cv=kfold, n_jobs=-1)
    print("MSE: '%.3g'" % (results_kfold_XGB.mean()))

    params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5],
        'n_estimators': [100, 500, 1000]
    }
    gridsearch = model_selection.GridSearchCV(model_kfold_XGB, params, scoring='neg_mean_squared_error', n_jobs=-1,
                              cv=kfold.split(train_inputs, train_outputs), verbose=3)

    gridsearch.fit(train_inputs, train_outputs)
    metadata['timestamp'] = str(datetime.datetime.now())
    metadata['features'] = list(gridsearch.feature_names_in_)
    metadata['best_score'] = gridsearch.best_score_
    metadata['metric'] = gridsearch.scoring
    metadata['params'] = gridsearch.best_params_
    test_preds = gridsearch.predict(test_inputs)
    test['preds'] = test_preds
    test = test[['home_team', 'away_team', 'away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa',
                 'div_game', 'spread_line', 'result', 'preds', 'home_spread_odds', 'away_spread_odds']]
    test = test.reset_index(drop=True)
    test['pick'] = np.where(test['spread_line'] < test['preds'], 'home', 'away')
    test['correct_pick'] = np.where(test['spread_line'] < test['result'], 'home', 'away')
    test['itm'] = np.where(test['pick'] == test['correct_pick'], 1, 0)
    test['money_gained'] = np.where(test['itm'] == 0, -100,
                                          np.where(test['pick'] == 'home',
                                                   np.where(test['home_spread_odds'] < 0, 100*100/abs(test['home_spread_odds']),
                                                            test['home_spread_odds']),
                                                   np.where(test['away_spread_odds'] < 0, 100*100/abs(test['away_spread_odds']),
                                                            test['away_spread_odds'])))
    test.dropna(inplace=True)
    design_experiment(test.reset_index(), metadata)
train_model()
data = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\NFL_Predictions_Upwork\\feature_frame.csv')
train = data[np.isin(data['season'], [2013, 2014, 2015])]
test = data[~np.isin(data['season'], [2013, 2014, 2015])]


train_inputs = train[['away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
train_outputs = train['result']
test_inputs = test[['away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
test_outputs = test['result']
print()
model_kfold_XGB = XGBRegressor()
kfold = KFold(n_splits=10)

results_kfold_XGB = model_selection.cross_val_score(model_kfold_XGB, train_inputs, train_outputs,
                                                scoring='neg_mean_squared_error', cv=kfold, n_jobs=-1)
print("MSE: '%.3g'" % (results_kfold_XGB.mean()))

model_kfold_XGB.fit(train_inputs, train_outputs)
test_preds = model_kfold_XGB.predict(test_inputs)
test['preds'] = test_preds
test = test[['home_team', 'away_team', 'away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa',
             'div_game', 'spread_line', 'result', 'preds', 'home_spread_odds', 'away_spread_odds']]
test = test.reset_index(drop=True)
test['pick'] = np.where(test['spread_line'] < test['preds'], 'home', 'away')
test['correct_pick'] = np.where(test['spread_line'] < test['result'], 'home', 'away')
test['itm'] = np.where(test['pick'] == test['correct_pick'], 1, 0)
test['money_gained'] = np.where(test['itm'] == 0, -100,
                                      np.where(test['pick'] == 'home',
                                               np.where(test['home_spread_odds'] < 0, 100*100/abs(test['home_spread_odds']),
                                                        test['home_spread_odds']),
                                               np.where(test['away_spread_odds'] < 0, 100*100/abs(test['away_spread_odds']),
                                                        test['away_spread_odds'])))
test.dropna(inplace=True)

best_picks = test.loc[np.where(abs(test['preds'] - test['spread_line']) > 10)[0],:]

inputs = data[['away_rest', 'home_rest', 'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
outputs = data['result']
model_kfold_XGB_full = XGBRegressor()
results_kfold_XGB_full = model_selection.cross_val_score(model_kfold_XGB_full, inputs, outputs,
                                                scoring='neg_mean_squared_error', cv=kfold, n_jobs=-1)
print("MSE: '%.3g'" % (results_kfold_XGB_full.mean()))

model_kfold_XGB_full.fit(train_inputs, train_outputs)

pickle.dump(model_kfold_XGB_full, open('C:\\Users\\Andrew Moss\\PycharmProjects\\NFL_Predictions_Upwork\\spread_calc.sav', 'wb'))
