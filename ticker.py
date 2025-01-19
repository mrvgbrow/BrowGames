#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import random


class Ticker():
    def __init__(self,name,duration,loop=0):
        self.name=name
        self.duration=duration
        self.loop=loop
        self.reset()

    def reset(self):
        self.count=self.duration
        self.loop_count=0

    def update(self):
        if self.count>0:
            self.count-=1
        else:
            if self.loop_count!=self.loop:
                self.count=self.duration
                self.loop_count+=1

    def is_finished(self):
        if self.count==0 and self.loop_count==self.loop:
            return True
        return False

    def finish(self):
        self.count=0
        self.loop_count=self.loop

