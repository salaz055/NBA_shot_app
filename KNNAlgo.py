# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:57:02 2022

@author: salaz
"""

import numpy as np
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import matplotlib.pyplot as plt
import nbashots as nba
import seaborn as sns
import time


nba_players = players.get_players()
#print(f"{len(nba_players)} total nba players")

active_players = [player for player in nba_players if player['is_active'] == True]

#print(f"{len(active_players)} active nba players")

active_players_df = pd.DataFrame(active_players)
active_players_df['zipped_id_name'] = list(zip(active_players_df.id, active_players_df.full_name))


active_players_df_with_stats_list = []
for player in active_players_df['zipped_id_name'].to_list():
    player_stats = {}
    player_stats['id'] = player[0]
    player_stats['full_name'] = player[1]
    
    
    # Average Statistics over Career
    player_career_df = playercareerstats.PlayerCareerStats(player_id= f'{player[0]}').get_data_frames()[0]
    
    # Creating Per Game Statistics
    player_career_df['AST/GP'] = player_career_df['AST'] / player_career_df['GP']
    player_career_df['FGA/GP'] = player_career_df['FGA'] / player_career_df['GP']
    player_career_df['REB/GP'] = player_career_df['REB'] / player_career_df['GP']
    player_career_df['STL/GP'] = player_career_df['STL'] / player_career_df['GP']
    player_career_df['BLK/GP'] = player_career_df['BLK'] / player_career_df['GP']
    player_career_df['PTS/GP'] = player_career_df['PTS'] / player_career_df['GP']
    player_career_df['FG3A/GP'] = player_career_df['FG3A'] / player_career_df['GP']
    
    
    player_stats['Age'] = player_career_df['PLAYER_AGE'].max()
    player_stats['FG_PCT'] = player_career_df['FG_PCT'].mean()
    player_stats['FGA/GP'] = player_career_df['FGA/GP'].mean()
    player_stats['FG3A/GP'] = player_career_df['FG3A/GP'].mean()
    player_stats['FG3_PCT'] = player_career_df['FG3_PCT'].mean()
    player_stats['REB/GP'] = player_career_df['REB/GP'].mean()
    player_stats['AST/GP'] = player_career_df['AST/GP'].mean()
    player_stats['STL/GP'] = player_career_df['STL/GP'].mean()
    player_stats['PTS/GP'] = player_career_df['PTS/GP'].mean()
    
    print(player_stats['id'])
    active_players_df_with_stats_list.append(player_stats)
    time.sleep(1)



print(len(active_players_df_with_stats_list))





















