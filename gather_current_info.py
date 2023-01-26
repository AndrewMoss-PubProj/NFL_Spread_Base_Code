import nfl_data_py as nfl
import os
import pandas

os.chdir('C:\\Users\\Andrew Moss\\PycharmProjects\\NFL_Predictions_Upwork')
year = int(input("What season are you betting"))
week = int(input("What week are you betting"))
schedule = nfl.import_schedules(years=[year])
schedule = schedule[schedule['week'] == week].loc[:, ['away_team', 'home_team', 'away_rest',
                                                      'home_rest', 'div_game', 'home_qb_name', 'away_qb_name',
                                                      'away_moneyline',  'home_moneyline', 'spread_line',
                                                      'home_spread_odds', 'away_spread_odds']]
input_sheet = schedule[['away_team', 'home_team', 'away_rest', 'home_rest', 'div_game']]
input_sheet[['elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa']] = 0
input_sheet = input_sheet[['away_team', 'home_team', 'away_rest', 'home_rest',
                           'elo1_pre', 'elo2_pre', 'Home_ANYa', 'Away_ANYa', 'div_game']]
if not os.path.exists('NFL_Season_' + str(year) + '/'):
    os.mkdir('NFL_Season_' + str(year) + '/')
if not os.path.exists('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/'):
    os.mkdir('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/')

input_sheet.to_csv('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/' + 'input_sheet.csv')
schedule.to_csv('NFL_Season_' + str(year) + '/' + 'Week_' + str(week) + '/' + 'info_sheet.csv')

