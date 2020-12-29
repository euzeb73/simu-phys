# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:24:53 2020

@author: jimen
"""
import pygame
from forms import Circle,Square,Polygone

class Mass():
    def __init__(self,m=1,OM=[0,0],angle=0,v=[0,0],w=0,form='Circle'):
        self.m=m
        self.OM=pygame.math.Vector2(OM[0],OM[1])
        self.v=pygame.math.Vector2(v[0],v[1])
        self.w=w
        self.angle=angle
        self.linklist=[]
        self.visible=True
        if form=='Circle':
            self.form=Circle(self)
        elif form=='Square':
            self.form=Square(self)
    def draw(self,screen):
        if self.visible:
            self.form.draw(screen)
