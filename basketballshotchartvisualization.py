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
    print(team_ids)

    
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
                         marginals_color=cmap(.3) , size = (8 , 8)).savefig('joint_grid.png')

    
    
    
def create_heatmap(player_name , season_id , ax , f):
    
    final_player_df , league_avg = get_player_shotchartdetail(player_name = player_name, season_id = season_id)
    
    # create the colormap
    c = ["darkred","red","lightcoral","white", "palegreen","green","darkgreen"]
    v = [0, .15 ,.25, .33 , 0.45 , .55 ,1.]
    l = list(zip(v,c))
    cmap_heat = LinearSegmentedColormap.from_list('rg',l, N=256)
    
    heat_map = nba.heatmap(final_player_df.LOC_X, final_player_df.LOC_Y,final_player_df.SHOT_MADE_FLAG, bins = 5 , cmap = cmap_heat, title = f"{player_name.title()} efficiency {season_id} Season" , ax = ax , facecolor_alpha= 1)
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

if __name__ == '__main__':
    print('hello')
