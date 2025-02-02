#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import csv
import numpy
import os

class ScoreTable:
    def __init__(self,filename):
        self.filename=filename
        self.data=[]
        if os.path.isfile(filename):
            self.read_table()
        else:
            self.write_table_header()

    def write_table_header(self): 
        with open(self.filename,'w') as csv_file:
            writer=csv.writer(csv_file,delimiter=',')
            writer.writerow(['Player','Timestamp','Player 1 Score','Number of Games'])
            csv_file.close()

    def read_table(self): 
        self.data=[]
        with open(self.filename,'r') as csv_file:
            reader=csv.DictReader(csv_file)

            for row in reader:
                self.data.append(row)
            csv_file.close()

    def add_row(self,data_list): 
        with open(self.filename,'a') as csv_file:
            writer=csv.writer(csv_file,delimiter=',')
            writer.writerow(data_list)
            csv_file.close()
        self.read_table()

    def select_player(self,player_name):
        player1_scores=[]
        ngames_scores=[]
        player_dates=[]
        for row in self.data:
            if row['Player']==player_name:
                player1_scores.append(int(row['Player 1 Score']))
                ngames_scores.append(int(row['Number of Games']))
                player_dates.append(row['Timestamp'])
        return player1_scores,ngames_scores,player_dates

    def select_all(self):
        player1_scores=[]
        ngames_scores=[]
        player_dates=[]
        player_names=[]
        for row in self.data:
            player1_scores.append(int(row['Player 1 Score']))
            ngames_scores.append(int(row['Number of Games']))
            player_names.append(row['Player'])
            player_dates.append(row['Timestamp'])
        return player_names,player1_scores,ngames_scores,player_dates

    def print_player_best(self,player_name,maxshow=10):
        (player1_scores,ngames_scores,player_dates)=self.select_player(player_name)
        player1_scores=numpy.array(player1_scores)
        ngames_scores=numpy.array(ngames_scores)
        sort_index=(-player1_scores).argsort()[:maxshow]
        self.print_table_header()
        for index in sort_index:
            print('%16s %9d %9d %30s' % (player_name,player1_scores[index],ngames_scores[index],player_dates[index]))

    def print_all_best(self,maxshow=10):
        (player_names,player1_scores,ngames_scores,player_dates)=self.select_all()
        player1_scores=numpy.array(player1_scores)
        ngames_scores=numpy.array(ngames_scores)
        sort_index=(-player1_scores).argsort()[:10]
        self.print_table_header()
        for index in sort_index:
            print('%16s %9d %9d %30s' % (player_names[index],player1_scores[index],ngames_scores[index],player_dates[index]))

    def print_table_header(self):
        print('%16s %9s %9s %30s' % ('Player','P1 Score','# Games','Date'))
        print('%16s %9s %9s %30s' % ('------','--------','-------','----'))
