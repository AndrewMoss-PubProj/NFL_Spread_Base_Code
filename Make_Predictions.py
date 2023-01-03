import pandas as pd
import numpy as np
import pickle
import os

os.chdir('C:\\Users\\Andrew Moss\PycharmProjects\\NFL_Predictions_Upwork')
model_xgb = pickle.load(open('Spread_calc.sav', 'rb'))
model_xgb_features = model_xgb.get_booster().feature_names
year = int(input("What season are you betting"))
week = int(input("What week are you betting"))
data = pd.read_csv('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/' + 'input_sheet.csv').\
    drop(columns='Unnamed: 0')
info_sheet = pd.read_csv('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/' + 'info_sheet.csv').\
    drop(columns='Unnamed: 0')
input_frame = data.drop(columns=['home_team', 'away_team'])
info_sheet['projected_home_margin'] = model_xgb.predict(input_frame)
info_sheet['projected_home_margin'] = info_sheet['projected_home_margin'].round(2)
info_sheet['recommend_bet'] = np.where(info_sheet['spread_line'] - info_sheet['projected_home_margin'] < -10, 'home',
                                       np.where(info_sheet['spread_line'] - info_sheet['projected_home_margin'] > 10,
                                                'away', 'pass'))
info_sheet.to_csv('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/' + 'info_sheet.csv')