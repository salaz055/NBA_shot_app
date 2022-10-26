# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:23:51 2022

@author: salaz
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from basketballshotchartvisualization import get_player_shotchartdetail
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter

pd.options.mode.chained_assignment = None

    # AVERAGE shot distance
    # time remaining
    # period

def create_shot_distance_bar(player_name , season_id):
    player_df , league_avg = get_player_shotchartdetail(player_name, season_id)
    
    
    
    df = player_df[['SHOT_DISTANCE','GAME_DATE']]
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df['month'] = df.GAME_DATE.dt.month
    df['year'] = df.GAME_DATE.dt.year
    
    
    df['month-year'] = df['GAME_DATE'].dt.strftime('%Y-%b')
    
    grouped_by_month = df.groupby('month-year')['SHOT_DISTANCE'].agg(['mean','size', 'count'])
    grouped_by_month.index = pd.to_datetime(grouped_by_month.index).date
    grouped_by_month = grouped_by_month.sort_index(ascending = True)
    
    # # Creating a series for for xlabels
    grouped_by_month_x_labels = pd.to_datetime(pd.Series(grouped_by_month.index))
    grouped_by_month_x_labels = list(grouped_by_month_x_labels.dt.strftime('%b-%Y'))
    # print(grouped_by_month_x_labels)
    # print(type(grouped_by_month_x_labels[0]))
    
    
    fig, ax = plt.subplots()
    
    ind = np.arange(len(grouped_by_month.index))
    ax.bar(ind, grouped_by_month['mean'], width = 0.35)
    ax.set_xticks(ind, labels= grouped_by_month_x_labels)
    plt.axhline(y=grouped_by_month['mean'].mean(), color='black', linestyle='--')
    fig.suptitle(f'{player_name.title()} Shot Distances for {season_id} Season', fontweight ="bold")
    plt.xticks(rotation = 45)

def create_stacked_shot_selection_bar(player_name , season_id , ax):

    
    player_df , league_avg = get_player_shotchartdetail(player_name , season_id)
    
    df = player_df[['SHOT_ZONE_RANGE','GAME_DATE']]
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df['month-year'] = df['GAME_DATE'].dt.strftime('%b-%Y')
    
    grouped_by_month = df.groupby(['month-year' , 'SHOT_ZONE_RANGE']).agg(['count'])
    grouped_by_month_tuples = list(grouped_by_month.index)
    df_grouped_by_month = pd.DataFrame(grouped_by_month , index = pd.MultiIndex.from_tuples(grouped_by_month_tuples))
    df_grouped_by_month = df_grouped_by_month.unstack()
    df_grouped_by_month.fillna(0 , inplace = True)
    df_grouped_by_month.columns = df_grouped_by_month.columns.droplevel(0)
    df_grouped_by_month.columns = df_grouped_by_month.columns.droplevel(0)
    df_grouped_by_month.index = pd.to_datetime(df_grouped_by_month.index)
    df_grouped_by_month.sort_index(ascending = True , inplace = True)
    df_grouped_by_month.index = df_grouped_by_month.index.strftime('%b')
    for col in df_grouped_by_month.columns:
        df_grouped_by_month[col] = df_grouped_by_month[col].apply(np.int64)
    
    # df_grouped_by_month = df_grouped_by_month.loc[ : , ['Less Than 8 ft.' , '8-16 ft.' , '16-24 ft.' , '24+ ft.']]
    # print(df_grouped_by_month.head())
    color_dict = {'16-24 ft.' : '#ef5675' , '24+ ft.' : '#ffa600', '8-16 ft.' : '#7a5195', 'Back Court Shot' : 'red',
            'Less Than 8 ft.' : '#003f5c'}    

    df_grouped_by_month.plot(kind='bar', stacked=True , ax = ax , title = f"{player_name.title()} Shot Selection by Month {season_id} Season" , color = color_dict)
    # plt.title(f"{player_name.title()} Shot Selection by Month {season_id} Season")
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Number of Shots')
    ax.set_xlabel('Month')
    # ax.get_legend().set_bbox_to_anchor((1, 1))
    # handles, labels = ax.get_legend_handles_labels()
    
    # order = [2,3,1,4,0]
    # ax.legend([handles[i] for i in order] , [labels[i] for i in order])
    # print(labels)
    
f = Figure(figsize = (5,5) , dpi = 100)
ax = f.add_subplot(111)

create_stacked_shot_selection_bar('lebron james' , '2018-19' , ax = ax)





