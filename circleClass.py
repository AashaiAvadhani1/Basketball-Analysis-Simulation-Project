#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 19:50:47 2018

@author: aashaiavadhani
"""

class Circle():
    def __init__(self,xCor,yCor,jerseyNum,side,radius = 10):
        self.x = xCor
        self.y = yCor
        self.jerseyNum = jerseyNum
        self.radius = 15
        self.side = side

    def __draw__(self,canvas):
        radius2 = radius / 2
        canvas.create_oval(xCor- radius2, yCor - radius2, xCor + radius2, yCor + radius2)
        canvas.create_text(xCor, yCor,text = str(self.jerseyNum))
