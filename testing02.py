# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:11:41 2022

@author: salaz
"""

import os
from tkinter import *
import tkinter as tk
import customtkinter
from basketballshotchartvisualization import create_heatmap , create_jointgrid , create_hex_map , create_shot_chart, create_kde
import nba_api
from nba_api.stats.static import players

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PIL import ImageTk, Image 

ax= plt.gca()
draw_court(ax = ax, shotzone = True , lw = 4)
plt.show()
