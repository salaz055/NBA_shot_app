# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:25:44 2022

@author: salaz
"""

from tkinter import *
import os
print(os.getcwd())
import tkinter as tk
import customtkinter
from basketballshotchartvisualization import shot_chart_use , draw_court ,  create_heatmap , create_jointgrid , create_hex_map , create_shot_chart, create_kde , shot_chart
import nba_api
from nba_api.stats.static import players

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PIL import ImageTk, Image
from other_shot_data import shot_selection_by_period , career_data_summary , get_distance_df , find_similar_players
from dataset_wrangling import create_stacked_shot_selection_bar

from Missed_made_kde_charts import made_shot_kde , missed_shot_kde



os.chdir(r'C:\Users\salaz\OneDrive\Desktop\Projects\NBA')

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")
    
    width = 1200
    height = 520
    
    def __init__(self):
        super().__init__()
        
        self.title("NBA Application")
        self.geometry(f"{App.width}x{App.height}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        # Creating the 2 base frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=20)
        self.frame_left.grid(row=0, column=0, sticky="nswe" , padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self , corner_radius=20)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        # Setting the top label
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="NBA Application",
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Player:",
                                              text_font=("Roboto Medium", 14))
        self.label_2.grid(row=2, column=0, pady=10, padx=0)
        
        
        self.entry = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="Select a Player")
        self.entry.grid(row=2, column=1, pady=10, padx=20)
        
        
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Create Heatmap for FG%",
                                                command = self.button1_click)
        self.button_1.grid(row = 4, column=0, pady=10, padx=10 , columnspan = 2)
        
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Create Shot Selection by Period",
                                                command = self.button2_click)
        self.button_2.grid(row = 5, column=0, pady=10, padx=10 , columnspan = 2)
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Create Shot Chart for attempts",
                                                command = self.button3_click)
        self.button_3.grid(row = 6, column=0, pady=10, padx=10 , columnspan = 2)
        
        
        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Create KDE Jointplot for Attempts",
                                                command = self.button4_click)
        self.button_4.grid(row = 7, column=0, pady=10, padx=10 , columnspan = 2)
        
        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Create Shot Selection by Month Chart",
                                                command = self.button5_click)
        self.button_5.grid(row = 8, column=0, pady=10, padx=10 , columnspan = 2)
        
        self.year = customtkinter.StringVar(value="2016-17")
        self.year_select = customtkinter.CTkComboBox(master=self.frame_left,
                                     values=['2016-17' , '2017-18', '2018-19' ,'2019-20' ,'2020-21' ,'2021-22'],
                                     variable=self.year)
        self.year_select.grid(row = 3, column=0, pady=10, padx=10, columnspan = 2)
        
        self.button_6 = customtkinter.CTkButton(master=self.frame_left,
                                                width=120,
                                                height=32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Show Career Statistics",
                                                command = self.button6_click)
        self.button_6.grid(row = 9, column=0, pady=10, padx=10 , columnspan = 2)

        
        

        
    def on_closing(self, event=0):
        print('quit')
        self.quit()
        self.destroy()

        
    def button1_click(self):

        window = customtkinter.CTkToplevel(self)
        window.geometry("600x550")
        
        f = Figure(figsize = (5,5) , dpi = 100)
        ax = f.add_subplot(111)
        
        create_heatmap(self.entry.get().lower(), self.year.get() , ax = ax , f = f)
        
        
        
        canvas = FigureCanvasTkAgg(f , master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        window.title(f'{self.entry.get().title()} Heatmap')
        
    
        
    def button2_click(self):
        
        window = customtkinter.CTkToplevel(self)
        window.geometry("750x550")
        
        f = Figure(figsize = (5,5) , dpi = 100)
        ax = f.add_subplot(111)
        
        
        shot_selection_by_period(self.entry.get().lower(), season_id = self.year.get(), ax = ax)
        
        
        canvas = FigureCanvasTkAgg(f , master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        window.title(f'{self.entry.get().title()} KDE')
        
    def button3_click(self):
        
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x650")
        
        f = Figure(figsize = (5,5) , dpi = 100)
        ax = f.add_subplot(111)
        
        shot_chart_use(self.entry.get().lower(), self.year.get() , ax)
        #f.colorbar(hex_map)
        
        
        canvas = FigureCanvasTkAgg(f , master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        window.title(f'{self.entry.get().title()} Shot Chart')
        
        toolbar = NavigationToolbar2Tk(canvas,
                                   window)
        
        toolbar.update()
        canvas.get_tk_widget().pack()
        
        get_distance_df(self.entry.get().lower() , self.year.get() , frame = window)
    
    def button4_click(self):
        self.button_4_window = customtkinter.CTkToplevel(self)
        self.button_4_window.geometry("590x710")
            
        create_jointgrid(self.entry.get().lower(), self.year.get())
        
        im = Image.open('joint_grid.png')
        self.frame_top_button_4 = customtkinter.CTkFrame(master=self.button_4_window,
                                                 height=0.8,
                                                 corner_radius=20)
        self.frame_bot_button_4 = customtkinter.CTkFrame(master=self.button_4_window,
                                                 height=0.2,
                                                 corner_radius=20)
        
        self.frame_top_button_4.grid(row=0, column=0, sticky="nswe" , padx=20, pady=20)
        self.frame_bot_button_4.grid(row=1, column=0, sticky="nswe" , padx=20, pady=20)
        
        ph = ImageTk.PhotoImage(im , master=self.frame_top_button_4)

        label = Label(self.frame_top_button_4, image=ph)

        label.image=ph
        label.pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        
        self.made_shots_button_4 = customtkinter.CTkButton(master = self.frame_bot_button_4,
                                                           width = 120,
                                                           height = 32,
                                                           border_width=0,
                                                           corner_radius=8,
                                                           text = "See Made Shots KDE" ,
                                                           command = self.made_shots_button_4_click)
        
        self.missed_shots_button_4 = customtkinter.CTkButton(master = self.frame_bot_button_4,
                                                           width = 120,
                                                           height = 32,
                                                           border_width=0,
                                                           corner_radius=8,
                                                           text = "See Missed Shots KDE",
                                                           command = self.missed_shots_button_4_click)
        
        self.made_shots_button_4.grid(row = 0 , column = 1 , sticky = "nswe" , padx = 20  , pady = 20)
        self.missed_shots_button_4.grid(row = 0 , column = 0, sticky = "nswe" , padx = 20  , pady = 20)
        
        
        self.button_4_window.title(f'{self.entry.get().title()} KDE for attempts during {self.year.get()} Season')
        
    def button5_click(self):
        
        window = customtkinter.CTkToplevel(self)
        window.geometry("550x550")
        
        f = Figure(figsize = (2,2) , dpi = 100)
        ax = f.add_subplot(111)
        
        create_stacked_shot_selection_bar(self.entry.get().lower(),self.year.get() , ax = ax)
        
        canvas = FigureCanvasTkAgg(f , master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        
        window.title(f'{self.entry.get().title()} Shot Selection by Month')
    
    def button6_click(self):
        self.frame_right_top = customtkinter.CTkFrame(master=self.frame_right,
                                                 height=0.8,
                                                 corner_radius=20)
        self.frame_right_bot = customtkinter.CTkFrame(master=self.frame_right,
                                                 height=0.2,
                                                 corner_radius=20)
        
        self.frame_right_top.grid(row=0, column=0, sticky="nswe" , padx=20, pady=20)
        self.frame_right_bot.grid(row=1, column=0, sticky="nswe" , padx=20, pady=20)
        
        career_data_summary(self.entry.get().lower() , frame = self.frame_right_top)
        
        self.similar_players = [player.title() for player in find_similar_players(self.entry.get().lower())]
        self.similar_player = customtkinter.StringVar(value= self.similar_players[0])
        
        self.similar_players_select = customtkinter.CTkComboBox(master=self.frame_right_bot,
                                     values= self.similar_players,
                                     variable= self.similar_player)
        self.similar_players_select.grid(row = 0, column=1, pady=10, padx=10, columnspan = 1)
        
        self.similar_player_year = customtkinter.StringVar(value="2016-17")
        self.similar_player_year_select = customtkinter.CTkComboBox(master=self.frame_right_bot,
                                     values=['2016-17' , '2017-18', '2018-19' ,'2019-20' ,'2020-21' ,'2021-22'],
                                     variable=self.similar_player_year)
        self.similar_player_year_select.grid(row = 0, column= 2, pady=10, padx=10, columnspan = 1) 
        
        self.similar_players_button = customtkinter.CTkButton(master = self.frame_right_bot,
                                                           width = 120,
                                                           height = 32,
                                                           border_width=0,
                                                           corner_radius=8,
                                                           text = "View Shot Chart",
                                                           command = self.similar_players_button_click)
        
        
        self.similar_players_button.grid(row = 0 , column = 3 , pady=10, padx=10, columnspan = 1)
        
        
        self.similar_player_label = customtkinter.CTkLabel(master=self.frame_right_bot,
                                              text="Similar Player Comparison",
                                              text_font=("Roboto Medium", -16))
        
        self.similar_player_label.grid(row=0, column=4, pady=10, padx=10)
        
    
    def made_shots_button_4_click(self):
        self.made_window = customtkinter.CTkToplevel(self.button_4_window)
        self.made_window.geometry("590x710")
        
        made_shot_kde(player_name = self.entry.get().lower(), season_id = self.year.get())
        
        im = Image.open('made_joint_grid.png')
        ph = ImageTk.PhotoImage(im , master=self.made_window)
        label = Label(self.made_window, image=ph)
        
        label.image=ph
        label.pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        
        self.made_window.title(f'{self.entry.get().title()} KDE made shots Season: {self.year.get()}')
        
    def missed_shots_button_4_click(self):
        self.missed_window = customtkinter.CTkToplevel(self.button_4_window)
        self.missed_window.geometry("590x710")
        
        missed_shot_kde(player_name = self.entry.get().lower(), season_id = self.year.get())
        
        im = Image.open('missed_joint_grid.png')
        ph = ImageTk.PhotoImage(im , master=self.missed_window)
        label = Label(self.missed_window, image=ph)
        
        label.image=ph
        label.pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        
        self.missed_window.title(f'{self.entry.get().title()} KDE missed shots Season: {self.year.get()}')
    
    def similar_players_button_click(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x650")
        
        f = Figure(figsize = (5,5) , dpi = 100)
        ax = f.add_subplot(111)
        
        shot_chart_use(self.similar_player.get().lower(), self.similar_player_year.get() , ax)
        
        
        canvas = FigureCanvasTkAgg(f , master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP , fill = tk.BOTH , expand = True)
        window.title(f'{self.similar_player.get().title()} Shot Chart for {self.similar_player_year.get()} Season')
        
        toolbar = NavigationToolbar2Tk(canvas, window)
        
        toolbar.update()
        canvas.get_tk_widget().pack()
        
        get_distance_df(self.similar_player.get().lower() , self.similar_player_year.get() , frame = window)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()