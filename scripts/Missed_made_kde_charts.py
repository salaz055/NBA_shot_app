# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:16:33 2022

@author: salaz
"""
import numpy as np
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats


from matplotlib import cm
from matplotlib.patches import Circle , Rectangle , Arc , ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap , ListedColormap ,  BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import nbashots as nba
import seaborn as sns
from matplotlib.figure import Figure
from basketballshotchartvisualization import get_player_shotchartdetail
from  matplotlib.colors import LinearSegmentedColormap
import customtkinter

from PIL import ImageTk, Image
import os

cmap_red = plt.cm.gist_heat_r
cmap_greens = LinearSegmentedColormap.from_list('greens', [ '#FFFFFF', '#98bf9e' , '#759e77' , '#5d885c' , '#527e50' , '#477444' , '#3b6937' , '#2e5d2a' , '#1e511b' , '#244a24'])


player_name = 'andrew wiggins'
season_id = '2020-21'


final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
# made_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] ==1]
# missed_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] == 0]

# nba.shot_chart_jointgrid(missed_shots.LOC_X, missed_shots.LOC_Y,
#                       title=f"{player_name.title()} Missed Shots for {season_id} Season",
#                       joint_type="kde", cmap = cmap_greens,
#                       marginals_color=cmap_greens(.4) , figsize = (300/96 , 300/96) , dpi = 60).savefig('joint_grid.png' , dpi = 60)

def missed_shot_kde(player_name , season_id):
    cmap_red =plt.cm.gist_heat_r
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    missed_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] == 0]
    return nba.shot_chart_jointgrid(missed_shots.LOC_X, missed_shots.LOC_Y,
                          title=f"{player_name.title()} Missed Shots for {season_id} Season",
                          joint_type="kde", cmap = cmap_red,
                          marginals_color=cmap_red(.3) , size = (8 , 8)).savefig('missed_joint_grid.png')


def made_shot_kde(player_name,  season_id):
    cmap_greens = LinearSegmentedColormap.from_list('greens', [ '#FFFFFF', '#98bf9e' , '#759e77' , '#5d885c' , '#527e50' , '#477444' , '#3b6937' , '#2e5d2a' , '#1e511b' , '#244a24'])
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    made_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] ==1]
    return nba.shot_chart_jointgrid(made_shots.LOC_X, made_shots.LOC_Y,
                          title=f"{player_name.title()} Made Shots for {season_id} Season",
                          joint_type="kde", cmap = cmap_greens,
                          marginals_color=cmap_greens(.4) , size = (8 , 8)).savefig('made_joint_grid.png')


missed_shot_kde('lebron james' , '2020-21')



