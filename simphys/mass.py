# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:24:53 2020

@author: jimen
"""
import pygame

from .forms import Circle, Square, Polygone
from math import sqrt


class Mass():
    def __init__(self, m=1, OM=[0, 0], angle=0, v=[0, 0], w=0, form='Circle'):
        self.m = m
        self.OM = pygame.math.Vector2(OM[0], OM[1])
        self.v = pygame.math.Vector2(v[0], v[1])
        self.w = w
        self.angle = angle
        self.size = 0.1
        self.linklist = []
        self.collides = True
        if form == 'Circle':
            self.form = Circle(self)
        elif form == 'Square':
            self.form = Square(self)

    def set_size(self, size):
        self.size = size
        self.form.size = size

    def save_state(self):
        self.typeinfo = dict()
        # Attributs de la masse
        self.typeinfo['m'] = self.m
        self.typeinfo['size'] = self.size
        self.typeinfo['collides'] = self.collides
        self.typeinfo['form'] = type(self.form)
        self.typeinfo['visible'] = self.form.visible
        # Paramètres cinématiques
        self.state = dict()
        self.state['OM'] = self.OM
        self.state['v'] = self.v
        self.state['angle'] = self.angle
        self.state['w'] = self.w

    def load_mass(self, typeinfo, state):
        # Attributs de la masse
        self.m = typeinfo['m']
        self.set_size(typeinfo['size'])
        self.collides = typeinfo['collides']
        self.form = Circle(self)  # à changer plus tard ?
        self.form.visible = typeinfo['visible']

        self.load_state(state)

    def load_state(self, state):
        # Paramètres cinématiques
        self.OM = state['OM']
        self.v = state['v']
        self.angle = state['angle']
        self.w = state['w']

    def restart(self):
        # A reecrire ou faire un load state.
        pass

    def sumforces(self, exceptrigid=False):
        # somme des forces
        force = pygame.math.Vector2(0, 0)
        for link, num in self.linklist:
            if not exceptrigid:  # Si on prend tout on somme tout le tps
                if num == 1:
                    force += link.force1
                elif num == 2:
                    force += link.force2
            elif not link.rigid:  # Sinon on ne somme que si c'est pas un rigid
                if num == 1:
                    force += link.force1
                elif num == 2:
                    force += link.force2
        return force

    def updatev(self, dt):

        force = self.sumforces()
        self.dv = (dt*force/self.m)
        self.v = self.v+self.dv

    def updateOM(self, dt):
        # Mise à jour de position une fois les 'bonnes vitesses' calculées si besoin
        self.OM = self.OM+dt*self.v

    def detect_bounce(self, world, dt):
        '''dt pour remonter les positions d'un cran: avant que ça se touche'''
        '''TODO faire un bon calcul des positions corrigées
        (pas que corriger une coordonnée)'''
        limite = world.sizex-self.size
        x0 = self.OM[0]-self.v[0]*dt
        y0 = self.OM[1]-self.v[1]*dt
        if self.OM[0] > limite:
            self.OM[0] = limite
            self.OM[1] = y0+self.v[1]*(limite-x0)/self.v[0]
            self.v[0] = -self.v[0]
        limite = self.size
        if self.OM[0] < limite:
            self.OM[0] = limite
            self.OM[1] = y0+self.v[1]*(limite-x0)/self.v[0]
            self.v[0] = -self.v[0]
        limite = world.sizey-self.size
        if self.OM[1] > limite:
            self.OM[0] = x0+self.v[0]*(limite-y0)/self.v[1]
            self.OM[1] = limite
            self.v[1] = -self.v[1]
        limite = self.size
        if self.OM[1] < limite:
            self.OM[0] = x0+self.v[0]*(limite-y0)/self.v[1]
            self.OM[1] = limite
            self.v[1] = -self.v[1]

    def handle_collision(self, mass, dt):
        '''dt pour remonter les positions d'un cran: avant que ça se touche'''
        collision = self.detect_collision(mass)
        if collision:
            # on change les vitesses
            # https://physics.stackexchange.com/questions/107648/what-are-the-general-solutions-to-a-hard-sphere-collision
            # permet de faire les calculs avec les 3 conservations
            # en fait la conservation du moment cinétique amène avec celle de l'impulsion que la diff de vitesse pour
            # les masses est colinéaire à l'axe passant par les centres des boules.
            # Après on exprime les nvelles vitesse avec les ancienne+- la même d'impulsion divisée par masse
            # dans la conservation de l'EC ça donne le résultat utilisé.
            x10 = self.OM-self.v*dt
            x20 = mass.OM-mass.v*dt
            M2M10 = x10-x20
            dmin = self.size+mass.size
            v1 = self.v
            v2 = mass.v
            dv = v2-v1
            if dv.length() > 0:
                deltat = -(M2M10.dot(dv)+sqrt((M2M10.dot(dv))**2 -
                           dv.dot(dv)*(M2M10.dot(M2M10)-dmin**2)))/dv.dot(dv)
                x1 = x10+v1*deltat
                x2 = x20+v2*deltat
                m1 = self.m
                m2 = mass.m
                M2M1 = x1-x2
                if M2M1.length() > 0:
                    n = M2M1.normalize()
                    P = 2*(n.dot(v2-v1)/(1/m1+1/m2))*n  # Variation d'impulsion
                    self.v += P/m1
                    mass.v -= P/m2

    def detect_collision(self, mass):
        collision = False
        d = (self.OM-mass.OM).length()
        if d <= self.size+mass.size:
            collision = True
        return collision

    def draw(self, screen):
        self.form.draw(screen)
