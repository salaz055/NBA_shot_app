# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:39:34 2022

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
from basketballshotchartvisualization import get_player_shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import tkinter as tk
from tkinter import ttk
import pandas as pd



def shot_selection_by_period(player_name , season_id , ax):
    player_df , league = get_player_shotchartdetail(player_name , season_id)
    
    df = player_df[['PERIOD','SHOT_ZONE_RANGE', 'GAME_DATE']]
    df_grouped = df.groupby(['PERIOD' , 'SHOT_ZONE_RANGE']).agg('count')
    grouped_by_period_tuples = list(df_grouped.index)
    df_grouped_by_period = pd.DataFrame(df_grouped, index = pd.MultiIndex.from_tuples(grouped_by_period_tuples)).unstack()
    col_names = []
    
    df_grouped_by_period.fillna(0 , inplace = True)    
    for col in df_grouped_by_period.columns:
        col_names.append(col[1])
        df_grouped_by_period[col] = df_grouped_by_period[col].apply(np.int64)
       
    df_grouped_by_period.columns = col_names  
    df_grouped_by_period.plot(kind='bar', stacked=True , ax = ax , title = f"{player_name.title()} Shot Selection by Period {season_id} Season")

    

def career_data_summary(player_name , frame):
    # root = tk.Tk()
    # root.title('Treeview demo')
    # root.geometry('620x200')
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'].lower() == player_name][0]
    career = playercareerstats.PlayerCareerStats(player_dict['id'])
    
    career = career.get_data_frames()[0].loc[: , ['SEASON_ID' , 'TEAM_ABBREVIATION' , 'GP', 'FGM', 'FGA' , 'FG_PCT' , 'FG3M', 'FG3A',
    'FG3_PCT' , 'FTM', 'FTA', 'FT_PCT' , 'PTS']]
    
    career.columns = ['SEASON' , 'TM' , 'GP', 'FGM', 'FGA' , 'FG%' , 'FG3M', 'FG3A',
                      'FG3%' , 'FTM', 'FTA', 'FT%' , 'PTS']
    
    cols = list(career.columns)
    tree = ttk.Treeview(frame)
    ttk.Style().configure("Treeview", background="#292929", 
                          foreground="#FFFFFF", fieldbackground="#292929")
    tree.pack()
    tree["columns"] = cols
    tree['show'] = 'headings'
    
    for i in cols:
        tree.column(i, anchor="w" , width=50)
        tree.heading(i, text=i, anchor='w')
    
    for index, row in career.iterrows():
        tree.insert("",0,text=index,values=list(row))

    # root.mainloop()

def get_distance_df(player_name , season_id , frame):
    player_df , league = get_player_shotchartdetail(player_name, season_id)
    player_df = player_df[['SHOT_ZONE_RANGE']]
    player_df = pd.DataFrame(player_df['SHOT_ZONE_RANGE'].value_counts())
    player_df['Percent of Total'] = player_df['SHOT_ZONE_RANGE'] / player_df['SHOT_ZONE_RANGE'].sum()
    player_df['Percent of Total'] = round(player_df['Percent of Total'] * 100 ,2)
    #player_df = player_df.reindex(index = ['Less Than 8 ft.' , '8-16 ft.' , '16-24 ft.' , '24+ ft.' , 'Back Court Shot'])
    player_df.reset_index(inplace = True)
    player_df.columns = ['Shot Range' , 'Number of Shots' , 'Percentage of Total Shots']
    player_df.sort_values('Percentage of Total Shots' , ascending = True , inplace = True)
    print(player_df)
    
    # root = tk.Tk()
    # root.title('Treeview demo')
    # root.geometry('620x200')
    
    cols = list(player_df.columns)
    
    tree = ttk.Treeview(frame)
    ttk.Style().configure("Treeview", background="#292929", 
                          foreground="#FFFFFF", fieldbackground="#292929")
    tree.pack()
    tree["columns"] = cols
    tree['show'] = 'headings'
    
    tree.heading('Shot Range', text='Shot Range')
    tree.heading('Number of Shots' , text = 'Number of Shots')
    tree.heading('Percentage of Total Shots', text='Percentage of Total Shots')
    
    for index, row in player_df.iterrows():
        tree.insert("",0,text=index,values=list(row))
        
def find_similar_players(player_name):
    df = pd.read_csv('active_players_df_labels_lower.csv')
    label = int(df[df['full_name'] == player_name]['labels'].values)
    df_player_group = df[df['labels'] == label].sort_values('PTS/GP' , ascending = False).reset_index()
    player_index = int(df_player_group[df_player_group['full_name'] == player_name].index.values)
    
    if player_index < 5:
        player_range = np.arange(0 , 11, 1)
        similar_players = df_player_group.loc[np.logical_and(df_player_group.index.isin(player_range) , df_player_group['full_name'] != player_name)]['full_name'].tolist()
        
    elif player_index > len(df_player_group) - 5:
        player_range = np.arange(len(df_player_group) - 11, len(df_player_group), 1)
        similar_players = df_player_group.loc[np.logical_and(df_player_group.index.isin(player_range) , df_player_group['full_name'] != player_name)]['full_name'].tolist()
        
        
    else:
        player_range = np.arange(player_index - 5 , player_index + 6, 1)
        similar_players = df_player_group.loc[np.logical_and(df_player_group.index.isin(player_range) , df_player_group['full_name'] != player_name)]['full_name'].tolist()
    
    return similar_players
    

if __name__ == "__main__":
    sims = find_similar_players('draymond green')
    print(sims)
    