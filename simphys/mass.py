# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:24:53 2020

@author: jimen
"""
import pygame

from .forms import Circle, Square, Polygone


class Mass():
    def __init__(self, m=1, OM=[0, 0], angle=0, v=[0, 0], w=0, form='Circle'):
        self.m0 = m
        self.OM0 = pygame.math.Vector2(OM[0], OM[1])
        self.v0 = pygame.math.Vector2(v[0], v[1])
        self.w0 = w
        self.angle = angle
        self.linklist = []
        self.visible = True
        if form == 'Circle':
            self.form = Circle(self)
        elif form == 'Square':
            self.form = Square(self)
        self.restart()

    def restart(self):
        self.m = self.m0
        self.OM = self.OM0
        self.v = self.v0
        self.w = self.w0

    def draw(self, screen):
        if self.visible:
            self.form.draw(screen)
