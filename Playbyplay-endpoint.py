# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:01:34 2022

@author: salaz
"""

import nba_api
import pandas as pd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import tkinter as tk
import requests


# Query for the last regular season game where the Pacers were playing
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.static import teams

nba_teams = teams.get_teams()

wolves = [team for team in nba_teams if team['abbreviation'] == 'MIN'][0]
wolves_id = wolves['id']
print(wolves_id)
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=wolves_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)

games_dict = gamefinder.get_normalized_dict()['LeagueGameFinderResults']
games_df = pd.DataFrame(games_dict)
print(games_df.head())

from nba_api.stats.endpoints import playbyplay
df = playbyplay.PlayByPlay('0022101224').get_data_frames()[0]
#print(df.head(10)) #just looking at the head of the data