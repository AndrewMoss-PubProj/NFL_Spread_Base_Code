import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import timer
import pickle
from sklearn import model_selection
from sklearn.model_selection import KFold

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

