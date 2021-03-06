# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:23:08 2020

@author: jimen
"""

import pygame


class Form():
    def __init__(self, mass, color=(255, 0, 0)):
        self.mass = mass
        self.size = mass.size
        self.color = color
        self.visible = True

    def is_clicked(self):
        pass


class Circle(Form):
    def __init__(self, mass, color=(255, 0, 0)):
        super().__init__(mass, color)
        self.R = self.size

    def draw(self, screen):
        if self.visible:
            self.R = self.size
            center = screen.OMtopx(self.mass.OM)
            # pour avoir au moins un point
            radius = max(screen.mtopx(self.R), 1)
            pygame.draw.circle(screen.window, self.color, center, radius)


class Polygone(Form):
    def __init__(self, mass, color=(255, 0, 0), angle=0, n=3, listpoints=[]):
        super().__init__(mass, color)
        self.angle = angle
        self.n = n
        self.listpoints = listpoints

    def draw(self, screen):
        pass


class Square(Polygone):
    def __init__(self, mass, color=(255, 0, 0), angle=0, a=0.1):
        super().__init__(mass, color, angle, 4, [])
        self.a = a
#        self.listpoints=[[x-a,y-a],[x-a,y+a],[x+a,y-a],[x+a,y-a]]
