# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:18:00 2022

@author: salaz
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nba_api as nba
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamplayerdashboard
df = pd.read_csv(r'dataset_creation\active_players_df_with_stats.csv')
df = df.dropna(axis = 0)
df = df.drop('Unnamed: 0' , axis = 1)
print(df.shape)
#%%

fig, axes = plt.subplots(2 , 1 , figsize= (10 , 7))

sns.histplot(data = df , x = 'REB/GP' , ax = axes [0])
sns.boxplot(data = df , x = 'REB/GP' , ax = axes [1])

#%%


fig, axes = plt.subplots(2 , 1 , figsize= (10 , 7))

sns.histplot(data = df , x = 'STL/GP' , ax = axes [0])
sns.boxplot(data = df , x = 'STL/GP' , ax = axes [1])

#%%
df_correlations = df.drop('id' , axis = 1).corr()
plt.figure(figsize = (10, 7))
sns.heatmap(df_correlations , annot = True)

#%%
plt.figure(figsize = (10, 7))
sns.scatterplot(x = 'Age' , y = 'FG3A/GP' , data = df)

#%%
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import players
from nba_api.stats.static import teams


# def get_team(player_name):
#     nba_players = players.get_players()
#     player_id = [player for player in nba_players if player['full_name'].lower() == player_name][0]['id']
    
#     team = commonteamroster.CommonTeamRoster(team_id = '1610612740').get_data_frames()[0]
#     return team['PLAYER'].tolist()

df = pd.read_csv('active_players_2.csv')
df['Name'] = df['Name'].str.lower()
df.to_csv('active_players_teams_lower.csv')



def find_teammates(player_name):
    lower_player_name = player_name.lower()
    df = pd.read_csv('active_players_teams_lower.csv')
    player_team = df[df['Name'] == lower_player_name]['Team'].values[0]
    teammates = df[df['Team'] == player_team]['Name'].tolist()
    return [teammate.title() for teammate in teammates]











