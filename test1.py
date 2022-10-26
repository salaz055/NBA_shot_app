# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:56:48 2022

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
import os

os.chdir(r'C:\Users\salaz\OneDrive\Desktop\Projects\NBA')

from basketballshotchartvisualization import get_player_shotchartdetail


cmap=plt.cm.gist_heat_r

player , avg = get_player_shotchartdetail('James Harden', '2019-20')

print(player.columns)

#nba.shot_chart(lebron.LOC_X, lebron.LOC_Y,
                     #title="Lebron FGA 2019-20 Season",
                     #kind="hex", cmap=cmap)
#plt.show()



heatmap = nba.heatmap(player.LOC_X, player.LOC_Y,
                      player.SHOT_MADE_FLAG, bins= 15)

print(type(player.SHOT_MADE_FLAG))

fig = plt.gcf()
fig.colorbar(heatmap)
plt.title(f"{player['PLAYER_NAME'][0]} FG% by Location, 2015-16 Season")
plt.show()

