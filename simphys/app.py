# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:01:13 2020

@author: jimen
"""
import pygame
from .screen import Screen
from .world import World


class Font():
    def __init__(self, font=None, size=48):

        self.font = pygame.font.SysFont(font, size)  # initialise la police
        self.textdic = dict()  # Dictionnaire vide

    def addtext(self, text, txtname=None, color=(255, 0, 0)):
        '''fabrique une image(surface) associée à text prete à coller'''
        if txtname == None:
            self.textdic[text] = self.font.render(text, True, color)
        else:
            self.textdic[txtname] = self.font.render(text, True, color)


class App():
    def __init__(self, FPS=60):
        pygame.init()
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.world = World(1,1)  # à ajouter plus tard avec add_World
        self.screen=Screen() #la fenêtre d'affichage
        self.set_speed(1)  # nb de fois la vitesse réelle

    def add_World(self, world):
        # Placer le WORLD dans l'app
        self.world = world
        self.world.dt = self.speed/self.FPS
        self.screen.set_world_size(world)

    def set_speed(self, speed):
        self.speed = speed
        self.world.dt = self.speed/self.FPS
        self.screen.change_speed(self.speed)
        
    def affiche_cmd(self):
        pass

    def affiche_pause(self):
        pass

    def run(self):
        
        stopped = False
        anim = False
        paused = True
        while stopped == False:

            # Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        anim = not(anim)
                        paused = not(paused)
                    if event.key == pygame.K_ESCAPE and paused:
                        stopped = True
                    if event.key == pygame.K_r and paused:
                        self.world.restart()
                    if event.key == pygame.K_f and paused:
                        self.screen.switch_full()
                    if event.key == pygame.K_UP:
                        self.FPS *= 1.5
                        self.set_speed(self.speed*2)
                    if event.key == pygame.K_DOWN:
                        self.FPS /= 1.5
                        self.set_speed(self.speed/2)

            if anim:
                self.world.update()
                self.screen.update(self.world)

            if paused:
                self.screen.affich_menu()
                self.screen.update(self.world)
            self.clock.tick(self.FPS)
        pygame.quit()
