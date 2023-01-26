import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from io import StringIO

def make_soup(thepage):
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

selenium_Path = "/home/andrewmoss/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("/home/andrewmoss/.config/google-chrome/Default")
driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
qb_list = ['Johnny Manziel', 'Ryan Lindley', 'Zach Mettenberger',
           'Seneca Wallace', 'Marcus Mariota', 'Tyrod Taylor', 'Matt Ryan',
           'Charlie Whitehurst', 'Ryan Mallett', 'Patrick Mahomes', 'Austin Davis',
           'A.J. McCarron', 'Christian Ponder', 'Brandon Weeden', 'Jake Locker', 'Jimmy Garoppolo',
           'DeShone Kizer', 'Jason Campbell', 'Kevin Hogan', 'Josh McCown', 'Matt McGloin', 'Eli Manning',
           'Mitch Trubisky', 'EJ Manuel', 'Blaine Gabbert', 'Derek Anderson', 'Tom Brady', 'Matt Moore',
           'Chase Daniel', 'Kellen Moore', 'Ryan Tannehill', 'Bryce Petty', 'Colin Kaepernick', 'Michael Vick',
           'Drew Stanton', 'Jeff Tuel', 'Drew Brees', 'Aaron Rodgers', 'Tony Romo', 'Jameis Winston',
           'Dak Prescott', 'Matt Flynn', 'Trevor Siemian', 'Connor Shaw', 'Matt Schaub', 'Jay Cutler',
           'Russell Wilson', 'Jimmy Clausen', 'Kyle Orton', 'T.J. Yates', 'Sam Bradford', 'Thaddeus Lewis',
           'Kellen Clemens', 'Brian Hoyer', 'Cody Kessler', 'Kirk Cousins', 'Josh Freeman', 'Nick Foles',
           'Geno Smith', 'Sean Mannion', 'Landry Jones', 'Carson Palmer', 'Ryan Fitzpatrick', 'Terrelle Pryor',
           'Derek Carr', 'Ben Roethlisberger', 'Mike Glennon', 'Andy Dalton', 'Chad Henne', 'Cam Newton',
           'Robert Griffin', 'Nathan Peterman', 'Connor Cook', 'Matt Cassel', 'Scott Tolzien', 'Joe Flacco',
           'Matt Barkley', 'C.J. Beathard', 'Matt Hasselbeck', 'Brock Osweiler', 'Carson Wentz', 'Brett Hundley',
           'Case Keenum', 'Paxton Lynch', 'Colt McCoy', 'Philip Rivers', 'Deshaun Watson', 'Andrew Luck',
           'Matthew Stafford', 'Mark Sanchez', 'Peyton Manning', 'Jared Goff', 'Blake Bortles', 'Luke McCown',
           'Shaun Hill', 'Tom Savage', 'Jacoby Brissett', 'Teddy Bridgewater', 'Alex Smith']
qb_list = [s.replace(' ', '-') for s in qb_list]

for player in qb_list:
    player = player.lower()
    # if os.path.isdir('Player_Game_Logs/' + player + '/'):
    #     continue
    for year in range(2005, 2023):
        year = str(year)

        url_string = 'https://www.fantasypros.com/nfl/games/'+player+'.php?season='+year
        driver.get(url_string)
        print(url_string)
        soup = make_soup(driver.page_source)
        player_data = ''
        for entry in soup.find_all('table'):
            if 'Player does not have any game data for the' in entry.text:
                print('No data for player in this year')
                continue
            for data in entry.find_all('tr'):
                if 'Totals' in data.text:
                    continue
                player_data = player_data + '\n'
                count = 0
                # item = ' '.join([i.capitalize() for i in player.split('-')])
                for time in data.find_all('td'):
                    if count == 0:
                        player_data = player_data + 'QB' + ',' + year + ','
                        player_data = player_data + time.text + ','
                    else:
                        if ',' in time.text:
                            value = time.text.split(',')
                            scores = value[1].split('-')
                            if len(scores) <= 1:
                                continue
                            if value[0] == 'W':
                                final_val = abs(int(scores[0]) - int(scores[1]))
                            else:
                                final_val = -1 * abs(int(scores[0]) - int(scores[1]))
                            player_data = player_data + str(final_val) + ','
                        elif count == 20:
                            player_data = player_data + time.text
                        else:
                            player_data = player_data + time.text + ','
                    count += 1
            if not os.path.isdir('Player_Game_Logs/' + player):
                os.mkdir(os.path.join(os.getcwd(), 'Player_Game_Logs/' + player))
            header = 'Position,Year,Week,Opp,Diff,Rating,Comp,Att,Comp%,pYds,YPA,pTD,pINT,Sacks,rAtt,rYds,YPC,rLong,' \
                     'rTD,Fum,FumL,fPoints, weekly_finish'
            player_data = pd.read_csv(StringIO(header + '\n' + player_data))
            player_data = player_data.fillna('-')
            player_data.to_csv(os.getcwd() + '/Player_Game_Logs/' + player + '/' + player + '-' + year + '.csv')
            break
