import nfl_data_py as nfl
import datapackage
import pandas as pd
import numpy as np
import glob
import os

# os.chdir(path)

def clean_inputs():
<<<<<<< HEAD
    data = nfl.import_schedules(years=[2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017])
=======
    data = nfl.import_schedules(years=[2013, 2014, 2015, 2016, 2017])
>>>>>>> 11ca6c88fa16e172aa26b6deae0b78f3105211f9
    data['game_id'] = data['game_id'].replace('SD', 'LAC', regex=True)
    data['game_id'] = data['game_id'].replace('_LA_', '_LAR_', regex=True)
    data['game_id'] = data['game_id'].replace('_LA$', '_LAR', regex=True)
    data['game_id'] = data['game_id'].replace('STL', 'LAR', regex=True)
    data['game_id'] = data['game_id'].replace('WAS', 'WSH', regex=True)


    print('schedules pulled')

    data_url = 'https://datahub.io/five-thirty-eight/nfl-elo/datapackage.json'

    # to load Data Package into storage
    package = datapackage.Package(data_url)

    # to load only tabular data
    resources = package.resources
    for resource in resources:
        print('fetching resource')
        if resource.tabular:
            elos = pd.read_csv(resource.descriptor['path'])
            break




    elos = elos[np.isin(elos['season'], [2013, 2014, 2015, 2016, 2017])]
    week_data_dict = dict(zip(data['gameday'], data['week']))
    elos['week'] = elos['date'].map(week_data_dict)
    elos['week'] = np.where(elos['week'] < 10, '0' + elos['week'].astype(str), elos['week'].astype(str))
    elos['code_1'] = elos['season'].astype(str) + '_' + elos['week'] + '_' + elos['team1'].str.upper() + '_' + elos['team2'].str.upper()
    elos['code_2'] = elos['season'].astype(str) + '_' + elos['week'] + '_' + elos['team2'].str.upper() + '_' + elos['team1'].str.upper()


    elos = pd.merge(data, elos[['code_2', 'elo1_pre', 'elo2_pre']],left_on='game_id',
                           right_on='code_2', how='left')
    elos = elos[elos['location'] !='Neutral'].drop(columns='code_2')

    qb_game_frame = pd.DataFrame()
<<<<<<< HEAD
    for files in glob.glob('Player_Game_Logs/*/*.csv'):
        temp = pd.read_csv(files)
        name = files.split('/')[1].replace('-', ' ').title()
=======
    for files in glob.glob('Player_Game_Logs\\*\\*.csv'):
        temp = pd.read_csv(files)
        name = files.split('\\')[6].replace('-', ' ').title()
>>>>>>> 11ca6c88fa16e172aa26b6deae0b78f3105211f9
        temp['name'] = name
        temp.drop('Week', axis=1, inplace=True)
        temp = temp.rename(columns={'Unnamed: 0': 'Week'})
        temp['Week'] = temp['Week'].astype(int) + 1
        qb_game_frame = pd.concat([qb_game_frame, temp])
    qb_game_frame = qb_game_frame[qb_game_frame['Att'] != '-']
    elos['Home_ANYa'] = elos.apply(lambda x: assign_anyas(x[['home_qb_name', 'season', 'week','gameday']],
                                                                  qb_game_frame), axis=1)
    elos['Away_ANYa'] = elos.apply(lambda x: assign_anyas(x[['away_qb_name', 'season', 'week', 'gameday']],
                                                                  qb_game_frame), axis=1)
    elos.to_csv('feature_frame.csv')

def assign_anyas(row, qb_game_frame):
    print(row['gameday'])
    try:
        game_frame = qb_game_frame[qb_game_frame['name'] == row['home_qb_name']]
    except:
        game_frame = qb_game_frame[qb_game_frame['name'] == row['away_qb_name']]
    game_frame = game_frame[(game_frame['Year'] < row['season']) |
                            ((game_frame['Year'] == row['season']) & (game_frame['Week'] < row['week']))]
    if len(game_frame) < 4:
        anya = 5.5
    else:
        anya = (sum(game_frame['pYds'].astype(float).astype(int)) + 20*sum(game_frame['pTD'].astype(float).astype(int)) - 45*sum(game_frame['pINT'].astype(float).astype(int))) / \
               (sum(game_frame['Att'].astype(float).astype(int)) + sum(game_frame['Sacks'].astype(float).astype(int)))
    return round(anya, 2)

clean_inputs()