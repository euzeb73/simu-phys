# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:23:08 2020

@author: jimen
"""

import pygame
from functions import OMtopx,mtopx

        
class Circle():
    def __init__(self,mass,color=(255,0,0),R=0.1):
        self.visible=True
        self.R=R
        self.mass = mass
        self.color = color
    def draw(self,screen):
        if self.visible:
            center=OMtopx(self.mass.OM)
            radius=max(mtopx(self.R),1) #pour avoir au moins un point
            pygame.draw.circle(screen,self.color,center,radius)
    def is_clicked(self):
        pass

class Polygone():
    def __init__(self,x,y,angle,n,listpoints):
        self.x=x
        self.y=y
        self.angle=angle
        self.n=n
        self.listpoints=listpoints
        self.colour = (255, 0, 0)
    def draw(self,screen):
        pass
    
class Square(Polygone):
    def __init__(self,mass,color=(255,0,0),a=0.1):
        self.a=a
        self.n=4
        self.color = color
#        self.listpoints=[[x-a,y-a],[x-a,y+a],[x+a,y-a],[x+a,y-a]]
