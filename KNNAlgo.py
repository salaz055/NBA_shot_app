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

