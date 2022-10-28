# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:18:00 2022

@author: salaz
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('active_players_df_with_stats.csv')
df = df.dropna(axis = 0)
df = df.drop('Unnamed: 0' , axis = 1)
print(df.columns)
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
