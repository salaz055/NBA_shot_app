# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 12:34:46 2022

@author: salaz
"""

import numpy as np
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
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

from  matplotlib.colors import LinearSegmentedColormap
import customtkinter
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

cmap=plt.cm.gist_heat_r

# defining the function

def get_player_shotchartdetail(player_name , season_id):
    
    # player dictionary
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'].lower() == player_name][0]

    
    career = playercareerstats.PlayerCareerStats(player_id = player_dict['id'])
    career_df = career.get_data_frames()[0]
    

    
    # team id during the season
    team_ids = list(career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID'])

    
    # shotchartdetail endpoints
    player_df = pd.DataFrame(columns = ['GRID_TYPE', 'GAME_ID', 'GAME_EVENT_ID', 'PLAYER_ID', 'PLAYER_NAME',
                                        'TEAM_ID', 'TEAM_NAME', 'PERIOD', 'MINUTES_REMAINING',
                                        'SECONDS_REMAINING', 'EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE',
                                        'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_DISTANCE',
                                        'LOC_X', 'LOC_Y', 'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG', 'GAME_DATE',
                                        'HTM', 'VTM'])
    for team_id in team_ids:
        shotchartlist = shotchartdetail.ShotChartDetail(team_id = int(team_id),
                                                        player_id = int(player_dict['id']),
                                                        season_type_all_star= 'Regular Season',
                                                        season_nullable= season_id,
                                                        context_measure_simple = 'FGA').get_data_frames()
        
        player_df = pd.concat([player_df, shotchartlist[0]] , ignore_index= True)
    
    
    
    player_df['SHOT_MADE_FLAG'] = player_df['SHOT_MADE_FLAG'].astype(np.int64)        
    player_df['LOC_X'] = player_df['LOC_X'].astype(np.int64)
    player_df['LOC_Y'] = player_df['LOC_Y'].astype(np.int64)
    player_df.drop_duplicates(inplace=True)
    
    return player_df , shotchartlist[1]
    

def draw_court(ax=None, color="blue", lw=1, shotzone=False, outer_lines=False):
    """Returns an axes with a basketball court drawn onto to it.
    This function draws a court based on the x and y-axis values that the NBA
    stats API provides for the shot chart data.  For example the center of the
    hoop is located at the (0,0) coordinate.  Twenty-two feet from the left of
    the center of the hoop in is represented by the (-220,0) coordinates.
    So one foot equals +/-10 units on the x and y-axis.
    Parameters
    ----------
    ax : Axes, optional
        The Axes object to plot the court onto.
    color : matplotlib color, optional
        The color of the court lines.
    lw : float, optional
        The linewidth the of the court lines.
    outer_lines : boolean, optional
        If `True` it draws the out of bound lines in same style as the rest of
        the court.
    Returns
    -------
    ax : Axes
        The Axes object with the court on it.
    """
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    
    # Draw shotzone Lines
    # Based on Advanced Zone Mode
    if (shotzone == True):
        inner_circle = Circle((0, 0), radius=80, linewidth=lw, color='black', fill=False)
        outer_circle = Circle((0, 0), radius=160, linewidth=lw, color='black', fill=False)
        corner_three_a_x =  Rectangle((-250, 92.5), 30, 0, linewidth=lw, color=color)
        corner_three_b_x = Rectangle((220, 92.5), 30, 0, linewidth=lw, color=color)
        
        # 60 degrees
        inner_line_1 = Rectangle((40, 69.28), 80, 0, 60, linewidth=lw, color=color)
        # 120 degrees
        inner_line_2 = Rectangle((-40, 69.28), 80, 0, 120, linewidth=lw, color=color)
        
        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle((53.20, 150.89), 290, 0, 70.53, linewidth=lw, color=color)
        inner_line_4 = Rectangle((-53.20, 150.89), 290, 0, 109.47, linewidth=lw, color=color)
        
        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle((130.54, 92.5), 80, 0, 35.32, linewidth=lw, color=color)
        inner_line_6 = Rectangle((-130.54, 92.5), 80, 0, 144.68, linewidth=lw, color=color)
        
        
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
    
    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)
        

    return ax
   

# The shot chart function
def shot_chart(data , title = '' , color = 'b' , xlim = (-250,250) , ylim= (422.5,-47.5) , line_color = 'blue', court_color = 'white' , court_lw = 2 , outer_lines = False , flip_court = False , gridsize = None , ax = None , despine = False , **kwargs):
    
    if ax is None:
        ax = plt.gca()
    
    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])
    
    ax.tick_params(labelbottom = 'off' , labelleft = 'off')
    ax.set_title(title , fontsize = 18)
    
    # Draw the court
    draw_court(ax , color = line_color , lw = court_lw , outer_lines=outer_lines, shotzone = True)
    
    # Seperate color by make or miss
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    Y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']
    
    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    Y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']
    
    # Plot the missed shots
    ax.scatter(x_missed, Y_missed , c = 'r' ,marker = 'x'  , s = 50, linewidths = 1 , )
    
    # plot the made shots
    ax.scatter(x_made, Y_made , facecolors = 'none', edgecolors = 'g' , marker = 'o' ,  s = 50, linewidths = 1)
    
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)
    
    if despine:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
    
def create_jointgrid(player_name , season_id):

    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)


    nba.shot_chart_jointgrid(final_player_df.LOC_X, final_player_df.LOC_Y,
                         title=f"{player_name.title()} FGA for {season_id} Season",
                         joint_type="kde", cmap=plt.cm.gist_heat_r,
                         marginals_color=cmap(.3) , size = (8 , 8)).savefig(r'images\joint_grid.png')

    
    
    
def create_heatmap(player_name , season_id , ax , f):
    
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    
    # create the colormap
    c = ["darkred","red","lightcoral","white", "palegreen","green","darkgreen"]
    v = [0, .15 ,.25, .33 , 0.45 , .55 ,1.]
    l = list(zip(v,c))
    cmap= plt.cm.gist_heat_r
    
    heat_map = nba.heatmap(final_player_df.LOC_X, final_player_df.LOC_Y,final_player_df.SHOT_MADE_FLAG , cmap = cmap, title = f"{player_name.title()} Efficiency {season_id} Season" , ax = ax)
    f.colorbar(heat_map)


def create_hex_map(player_name , season_id , ax):
    
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    
    nba.shot_chart(final_player_df.LOC_X, final_player_df.LOC_Y,
               kind="hex", title=f"{player_name.title()} FGA {season_id} Season",
               cmap=cmap, gridsize=26, ax = ax)
    
def create_shot_chart(player_name , season_id , ax):
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    
    nba.shot_chart(final_player_df.LOC_X, final_player_df.LOC_Y,
              title=f"{player_name.title()} Shots {season_id} Season" , marker = 'o' , s = 10 , ax = ax)

def create_kde(player_name , season_id , ax):
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    
    nba.shot_chart(final_player_df.LOC_X, final_player_df.LOC_Y,
               kind="kde", title=f"{player_name.title()} Shot Attempts KDE {season_id} Season", alpha = 0.75, color = 'b', court_lw = 1, court_color='black', levels = 10 , ax = ax)


def draw_court_1(ax=None, color="blue", lw=1, shotzone=False, outer_lines=False):
    
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    
    # Draw shotzone Lines
    # Based on Advanced Zone Mode
    if (shotzone == True):
        inner_circle = Circle((0, 0), radius=80, linewidth=lw, color='black', fill= True , alpha = 0.5)
        outer_circle = Circle((0, 0), radius=160, linewidth=lw, color='black', fill=False)
        corner_three_a_x =  Rectangle((-250, 92.5), 30, -140, linewidth=lw, color='red' , fill = True , alpha = 0.5)
        corner_three_b_x = Rectangle((220, 92.5), 30, 0, linewidth=lw, color='red' , fill = True)
        
        # 60 degrees
        inner_line_1 = Rectangle((40, 69.28), 80, 0, 60, linewidth=lw, color='red' , fill = True)
        # 120 degrees
        inner_line_2 = Rectangle((-40, 69.28), 80, 0, 120, linewidth=lw, color=color)
        
        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle((53.20, 150.89), 290, 0, 70.53, linewidth=lw, color=color)
        inner_line_4 = Rectangle((-53.20, 150.89), 290, 0, 109.47, linewidth=lw, color=color)
        
        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle((130.54, 92.5), 80, 0, 35.32, linewidth=lw, color=color)
        inner_line_6 = Rectangle((-130.54, 92.5), 80, 0, 144.68, linewidth=lw, color=color)
        
        
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
    
    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)
        

    return ax
        
    
def shot_chart_blank(title = '' , color = 'b' , xlim = (-250,250) , ylim= (422.5,-47.5) , line_color = 'grey', court_color = 'white' , court_lw = 2 , outer_lines = False , flip_court = False , gridsize = None , ax = None , despine = False , **kwargs):
    
    if ax is None:
        ax = plt.gca()
    
    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])
    
    ax.tick_params(labelbottom = 'off' , labelleft = 'off')
    ax.set_title(title , fontsize = 18)
    
    # Draw the court
    draw_court_1(ax , color = line_color , lw = court_lw , outer_lines=outer_lines, shotzone = True)

    
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)
    
    if despine:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)   


def shot_chart_use(player_name , season_id , ax):
    player_df , league = get_player_shotchartdetail(player_name = player_name , season_id = season_id)
    shot_chart(player_df , title = f'{player_name.title()} Shot Chart for {season_id} Season' , color= 'black' , line_color = 'black' , ax = ax)
    

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
    df_grouped_by_period.plot(kind='bar', stacked=True , ax = ax , title = f"{player_name.title()} Shot Selection by Period for {season_id} Season")

    

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
    df = pd.read_csv(r'datasets\active_players_df_labels_lower.csv')
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
    
def find_teammates(player_name):
    lower_player_name = player_name.lower()
    df = pd.read_csv(r'datasets\active_players_teams_lower.csv')
    player_team = df[df['Name'] == lower_player_name]['Team'].values[0]
    teammates = df[df['Team'] == player_team]['Name'].tolist()
    return [teammate.title() for teammate in teammates]

def missed_shot_kde(player_name , season_id):
    cmap_red =plt.cm.gist_heat_r
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    missed_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] == 0]
    return nba.shot_chart_jointgrid(missed_shots.LOC_X, missed_shots.LOC_Y,
                          title=f"{player_name.title()} Missed Shots for {season_id} Season",
                          joint_type="kde", cmap = cmap_red,
                          marginals_color=cmap_red(.3) , size = (8 , 8)).savefig(r'images\missed_joint_grid.png')


def made_shot_kde(player_name,  season_id):
    cmap_greens = LinearSegmentedColormap.from_list('greens', [ '#FFFFFF', '#98bf9e' , '#759e77' , '#5d885c' , '#527e50' , '#477444' , '#3b6937' , '#2e5d2a' , '#1e511b' , '#244a24'])
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    made_shots = final_player_df[final_player_df['SHOT_MADE_FLAG'] ==1]
    return nba.shot_chart_jointgrid(made_shots.LOC_X, made_shots.LOC_Y,
                          title=f"{player_name.title()} Made Shots for {season_id} Season",
                          joint_type="kde", cmap = cmap_greens,
                          marginals_color=cmap_greens(.4) , size = (8 , 8)).savefig(r'images\made_joint_grid.png')

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
    

    color_dict = {'16-24 ft.' : '#ef5675' , '24+ ft.' : '#ffa600', '8-16 ft.' : '#7a5195', 'Back Court Shot' : 'red',
            'Less Than 8 ft.' : '#003f5c'}    

    df_grouped_by_month.plot(kind='bar', stacked=True , ax = ax , title = f"{player_name.title()} Shot Selection by Month {season_id} Season" , color = color_dict)

    ax.set_ylabel('Number of Shots')
    ax.set_xlabel('Month')
    
def zone_chart(player_name , season_id , frame):
    # Add Frame
    zone_df = get_player_shotchartdetail(player_name , season_id)[0][['SHOT_ZONE_BASIC' , 'SHOT_MADE_FLAG']]
    zone_df_grouped = zone_df.groupby('SHOT_ZONE_BASIC')['SHOT_MADE_FLAG'].agg(['mean' , 'sum', 'size'])
    zone_df_grouped.reset_index(inplace = True)
    zone_df_grouped.columns = ['Shot Zone' , 'Shooting Percentage' , 'Shots Made' , 'Shots Taken']
    zone_df_grouped['Shooting Percentage'] = (zone_df_grouped['Shooting Percentage'] * 100).round(2)
    zone_df_grouped.sort_values('Shots Taken' , ascending = True , inplace = True)
    #print(zone_df_grouped.head(4))
    
    zone_cols = list(zone_df_grouped.columns)
    
    tree = ttk.Treeview(frame)
    ttk.Style().configure("Treeview", background="#292929", 
                          foreground="#FFFFFF", fieldbackground="#292929")
    tree.pack()
    tree["columns"] = zone_cols
    tree['show'] = 'headings'
    
    tree.heading('Shot Zone', text='Shot Zone')
    tree.heading('Shooting Percentage', text='Shooting Percentage')
    tree.heading('Shots Made' , text = 'Shots Made')
    tree.heading('Shots Taken', text='Shots Taken')
    
    for index, row in zone_df_grouped.iterrows():
        tree.insert("",0,text=index,values=list(row))




if __name__ == '__main__':
    #zone_chart('jaden mcdaniels' , '2022-23')
    
    
    
    
    
    
    
    
    
