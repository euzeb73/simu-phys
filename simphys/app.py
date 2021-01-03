# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:01:13 2020

@author: jimen
"""
import pygame
from . import values


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
    def __init__(self, displayw=800, displayh=600, FPS=60):
        values.HEIGHT = displayh
        values.WIDTH = displayw
        pygame.init()
        self.width = displayw
        self.height = displayh
        self.FPS = FPS
        self.fullscreen=False
        self.window = pygame.display.set_mode(
            (self.width, self.height))
        self.clock = pygame.time.Clock()
        self.world = None  # à ajouter avec add_World
        self.speed = 1  # nb de fois la vitesse réelle
        self.fontbig = Font('timesnewroman',36)  # initialise la police Grande
        self.fontsmall = Font('segoescript', 10)  # initialise la police petite
        self.fontmedium = Font('segoescript', 24) #la moyenne

    def add_World(self, world):
        # Placer le WORLD dans la fenetre

        if world.sizex >= world.sizey*4/3:  # bon rectangle
            values.PXPM = values.WIDTH/world.sizex  # Afficher sur toute la largeur
            values.YSHIFT = int((values.HEIGHT-world.sizey*values.PXPM)/2)
            values.XSHIFT = 0
        else:
            values.PXPM = values.HEIGHT/world.sizey  # Afficher sur toute la hauteur
            values.YSHIFT = 0
            values.XSHIFT = int((values.WIDTH-world.sizex*values.PXPM)/2)
        self.world = world
        self.world.dt = self.speed/self.FPS
        self.world.screen = self.window
        # le rectangle du monde
        width = min(values.WIDTH, int(world.sizex*values.PXPM))
        height = min(values.HEIGHT, int(world.sizey*values.PXPM))
        values.XMAX = values.XSHIFT+width
        values.YMAX = values.YSHIFT+height
        self.world.rect = pygame.Rect(
            values.XSHIFT, values.YSHIFT, width, height)
#        #On sauvegarde les CI
#        self.world.set_CI()

    def set_speed(self, speed):
        self.speed = speed
        self.world.dt = self.speed/self.FPS
        
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

    
    def affiche_cmd(self):
        pass

    def affiche_pause(self):
        pass

    def run(self):
        # Put all variables up here
        stopped = False
        anim = False
        paused = True

        # Prépare les affichages text
        self.fontbig.addtext('Pause')
        self.fontbig.addtext('Press ESC to QUIT', 'Quit')
        self.fontbig.addtext('Press R to RESTART', 'Restart')
        self.fontmedium.addtext('Press F to switch to FULLSCREEN','Fullscreen',(255,0,128))
        self.fontsmall.addtext('START/PAUSE : ENTER', 'Enter', (0, 0, 255))
        self.fontsmall.addtext('Speed up: KUP', 'Up', (0, 0, 255))
        self.fontsmall.addtext('Speed down: KDOWN', 'Down', (0, 0, 255))
        self.fontsmall.addtext('Speed {}'.format(
            self.speed), 'Speed', (0, 0, 255))

        # Tailles du monde:
        centerx = self.world.rect.centerx
        centery = self.world.rect.centery
        right = self.world.rect.right
        bottom = self.world.rect.bottom
        topleft = self.world.rect.topleft
        top = self.world.rect.top

        # Tuple for filling display... Current is lightgrey
        self.window.fill((150, 150, 150))
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
                        self.switch_full()
                    if event.key == pygame.K_UP:
                        self.FPS *= 1.5
                        self.set_speed(self.speed*2)
                    if event.key == pygame.K_DOWN:
                        self.FPS /= 1.5
                        self.set_speed(self.speed/2)

            if anim:
                self.world.draw()
                self.world.update()

            if paused:
                self.world.draw()
                surface = self.fontbig.textdic['Pause']
                w, h = surface.get_size()
                self.window.blit(surface, (centerx-w//2, centery-h//2))
                h2=h
                surface = self.fontmedium.textdic['Fullscreen']
                w, h = surface.get_size()
                self.window.blit(surface, (centerx-w//2, centery+2*h2))
                surface = self.fontbig.textdic['Quit']
                w, h = surface.get_size()
                self.window.blit(surface, (centerx-w//2, bottom-2*h))
                surface = self.fontbig.textdic['Restart']
                w, h = surface.get_size()
                self.window.blit(surface, (centerx-w//2, top+h))

            # Affichage des commandes et de la vitesse
            surface = self.fontsmall.textdic['Enter']
            w, h = surface.get_size()
            self.window.blit(surface, (right-w, top))
            surface = self.fontsmall.textdic['Up']
            w, h = surface.get_size()
            self.window.blit(surface, (right-w, top+h))
            surface = self.fontsmall.textdic['Down']
            w, h = surface.get_size()
            self.window.blit(surface, (right-w, top+2*h))
            # mise à jour de la vitesse
            self.fontsmall.addtext('Speed {}'.format(
                self.speed), 'Speed', (0, 0, 255))
            surface = self.fontsmall.textdic['Speed']
            w, h = surface.get_size()
            self.window.blit(surface, topleft)

            self.clock.tick(self.FPS)
            pygame.display.update()
        pygame.quit()
