# nba_application 

nba_application is a tool used to visualize shot distribuitions for players. The application allows users to create:

- Visualizations for any season from 2016-17 through the current season.
- Heatmaps for FG%
- Bar Charts for shot selection by quarter of the game and month.
- Shot Charts/KDE plot for attempts
- Career statistics tables

The tool also allows the user to find/compare similar players (found through KMeans) and quickly compare a player to their teammates.

![ezgif com-gif-maker(4)](https://user-images.githubusercontent.com/101416331/202031080-6759066d-6252-4519-bca5-931e64d41aae.gif)


## Career Statistics 
The career satistics button will prompt the app to show:
- The career statistics table for the player selected
- The similar player comparison tool: This includes a drop down menu to choose from 10 of the most similar players, a season/year dropdown, and a button to quickly create a shot chart for the similar player.
- The teammate comparison tool: This includes a drop down menu to choose from teammates for the player, a season/year dropdown, and a button to quickly create a shot chart for the teammate.

### Similar Player Comparison Tool
![ezgif com-gif-maker(3)](https://user-images.githubusercontent.com/101416331/202030267-67d038a3-5025-4bca-9afe-260ee5de6f44.gif)

### Teammate Comparison Tool
![ezgif com-gif-maker(5)](https://user-images.githubusercontent.com/101416331/202032771-1dddfc2b-f560-4e28-a2e0-6032a7ea0641.gif)



## Reference/Requirements:
- nbashots: https://github.com/savvastj/nbashots 
- nba_api: https://github.com/swar/nba_api
- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
- Other requirements are in the requirements.txt file
