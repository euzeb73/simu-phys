# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:26:03 2020

@author: jimen
"""

import pygame
import numpy as np
from .mass import Mass
from .links import LinkCsteF
from .functions import norm


class World():
    def __init__(self, sizex, sizey):
        self.sizex = sizex  # Taille du monde en m. le mieux c'est de respecter sizex=4/3 sizey
        self.sizey = sizey
        # le rectangle monde par défaut
        self.rect = pygame.Rect(0, 0, 1024, 768)
        self.mass = []
        self.link = []
        self.g = 9.81
        self.vecg = np.array([0, -self.g])
        self.color = (255, 255, 255)
        #self.screen = 0  # Il faudra mettre la surface pygame dans laquelle on affiche
        #                 # PAS utile en fait ?
        self.dt = 0.1
        self.gravity = True
        self.earth = Mass(1e24)
        self.earth.form.visible = False
        self.boucingbounds=True #(bords rebondissants)

    def restart(self):
        for mass in self.mass:
            mass.restart()
        for link in self.link:
            link.update()

    def add_Mass(self, m):
        '''Ajoute la masse et les liens qui lui sont associés au monde'''
        self.mass.append(m)
        if self.gravity:
            lien = LinkCsteF(m, self.earth, [0, -m.m*self.g])
            self.add_Link(lien)
        for link,num in m.linklist:
            if link not in self.link:
                self.link.append(link)

    def add_Link(self, l):
        ''' A n'utiliser que si on a ajouté des masses sans liens
        Utiliser add mass qui ajoute aussi les liens'''
        self.link.append(l)

    def enable_gravity(self, g):
        '''Si on active la gravité après avoir ajouté des masses
        pas utile normalement'''
        for mass in self.mass:
            lien = LinkCsteF(mass, self.earth, [0, -mass.m*self.g])
            self.add_Link(lien)

    def disable_gravity(self, masslist=[]):
        '''Desactive la gravité pour les mass de masslist
        ou pour toutes les masses si masslist est vide'''
        if masslist == []:
            masslist = self.mass
        for mass in masslist:
            for i in range(len(mass.linklist)):
                lien, num = mass.linklist[i]
                if num == 1:
                    if lien.mass2 == self.earth:
                        del mass.linklist[i]
                        self.link.remove(lien)
                else:
                    if lien.mass1 == self.earth:
                        del mass.linklist[i]
                        self.link.remove(lien)
    def detect_bounce(self):
        for mass in self.mass:
            mass.detect_bounce(self)

    def update(self):
        # Mise à jour des positions des masses
        for mass in self.mass:
            mass.updated=False #parce qu'on n'a pas encore updated la position
            mass.updatev(self.dt)
        for mass in self.mass:
            mass.updateOM(self.dt)
        #test collision des bords:
        if self.boucingbounds:
            self.detect_bounce()
            
        # Mise à jour des forces dans les liens
        for link in self.link:
            link.update()

    def draw(self,screen):
        window=screen.window
        pygame.draw.rect(window, (255, 255, 255), screen.worldrect)
        for l in self.link:
            l.draw(screen)
        for m in self.mass:
            m.draw(screen)
