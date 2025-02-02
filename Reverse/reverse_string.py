#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import csv
import numpy
import random
import os

class ReverseString:
    def __init__(self,length,nreverse):
        self.length=length
        self.init_string=self.init_digits()
        self.value=self.init_digits()
        self.do_reverses(nreverse)

    def init_digits(self):
        init_string=''
        for i in range(1,self.length+1):
            init_string+=str(i)
        return init_string

    def check_solved(self):
        if self.value==self.init_string:
            return 1
        return None

    def reset_string(self):
        self.value=self.init_digits()

    def reverse_digits(self,location):
        self.value=self.value[location-1::-1]+self.value[location:]

    def do_reverses(self,nreverse):
        while self.value==self.init_string:
            old_digit=0
            digit=0
            for i in range(0,nreverse):
                while digit == old_digit:     
                    digit=random.randrange(1,self.length+1)
                self.reverse_digits(digit)
                old_digit=digit
