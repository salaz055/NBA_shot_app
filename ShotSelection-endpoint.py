# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:16:04 2022

@author: salaz
"""


from nba_api.stats.endpoints import shotchartdetail

df = shotchartdetail.ShotChartDetail(team_id = '1610612750',player_id = '1630162',game_id_nullable= '0022101224' , context_measure_simple = 'FGA').get_data_frames()[0]
print(df)