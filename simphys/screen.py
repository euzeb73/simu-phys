# -*- coding: utf-8 -*-

import pygame
from .app import Font

class Screen():
    def __init__(self,width,height):
        self.width=width
        self.height =height
        self.fullscreen=False
        self.window=pygame.display.set_mode(
            (self.width, self.height))
        self.worldrect=pygame.Rect(0,0,self.width,self.height) #Rectangle du monde, par défaut toute la fenêtre
        self.pxpm=100 #pixel per meter échelle de conversion 
        self.fontbig = Font('timesnewroman',36)  # initialise la police Grande
        self.fontsmall = Font('segoescript', 10)  # initialise la police petite
        self.fontmedium = Font('segoescript', 24) #la moyenne
    def switch_full(self):
        if self.fullscreen:
            flag=0
            self.fontmedium.addtext('Press F to switch to FULLSCREEN','Fullscreen',(255,0,128))
        else:
            flag=pygame.FULLSCREEN
            self.fontmedium.addtext('Press F to switch to WINDOW mode','Fullscreen',(255,0,128))
        self.fullscreen=not(self.fullscreen)
        return pygame.display.set_mode(
            (self.width, self.height),flag)
    def set_world_size(self,world):
        ''' Ajuste les dimensions en pixels du monde par rapport aux dimensions de la fenêtre'''
        if world.sizex >= world.sizey*4/3:  # bon rectangle
            self.pxpm = self.width/world.sizex  # Afficher sur toute la largeur
            yshift = int((self.height-world.sizey*self.pxpm)/2)
            xshift = 0
            width=self.width
            height=int(world.sizey*self.pxpm)
        else:
            self.pxpm = self.height/world.sizey  # Afficher sur toute la hauteur
            yshift = 0
            xshift = int((self.width-world.sizex*self.pxpm)/2)
            width=int(world.sizex*self.pxpm)
            height=self.height
        
        # le rectangle du monde
        self.worldrect = pygame.Rect(
            xshift, yshift, width, height)


    def mtopx(dinm):
    ''' Convertit les distances en m vers des pixels'''
        return int(dinm*self.pxpm)


    def OMtopx(OM):
        '''Convertit les positions en m vers des coords en pixels
        Retourne un tuple '''
        xshift=self.worldrect[0]
        ymax=self.worldrect[1]+self.worldrect[3]
        return (self.mtopx(OM[0])+xshift, ymax-mtopx(OM[1]))


