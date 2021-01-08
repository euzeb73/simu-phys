# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:23:08 2020

@author: jimen
"""

import pygame

class Form():
    def __init__(self,mass,screen, color=(255, 0, 0)):
        self.mass = mass
        self.color = color
        self.screen=screen
        self.visible = True


    def is_clicked(self):
        pass

class Circle(Form):
    def __init__(self, mass,screen, color=(255, 0, 0), R=0.1):
        super().__init__(mass,screen,color)
        self.R = R
        

    def draw(self):
        if self.visible:
            center = self.screen.OMtopx(self.mass.OM)
            radius = max(self.screen.mtopx(self.R), 1)  # pour avoir au moins un point
            pygame.draw.circle(self.screen, self.color, center, radius)

   


class Polygone(Form):
    def __init__(self, mass,screen, color=(255, 0, 0), angle=0, n=3, listpoints=[]):
        super().__init__(mass,screen,color)
        self.angle = angle
        self.n = n
        self.listpoints = listpoints

    def draw(self, screen):
        pass


class Square(Polygone):
    def __init__(self, mass,screen, color=(255, 0, 0),angle=0, a=0.1):
        super().__init__(mass,screen,color,angle,4,[])
        self.a = a
#        self.listpoints=[[x-a,y-a],[x-a,y+a],[x+a,y-a],[x+a,y-a]]
