# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:24:53 2020

@author: jimen
"""
import pygame

from .forms import Circle, Square, Polygone
from .functions import norm

class Mass():
    def __init__(self, m=1, OM=[0, 0], angle=0, v=[0, 0], w=0, form='Circle'):
        self.m0 = m
        self.OM0 = pygame.math.Vector2(OM[0], OM[1])
        self.v0 = pygame.math.Vector2(v[0], v[1])
        self.w0 = w
        self.angle = angle
        self.rigidlink=None
        self.updated=False #pour voir si on a mis à jour la masse ou pas
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

    def updatev(self,dt):
        # somme des forces
        force = pygame.math.Vector2(0, 0)
        #belongtosolid=False
        for link, num in self.linklist:
            if not link.rigid:
                if num == 1:
                    force += link.force1
                elif num == 2:
                    force += link.force2
            # else:
            #     belongtosolid=True
            #     rigidlink=link #on n'est censé n'avoir qu'un lien solide
            #     #massnumonlink=num   #PAS utile ?

        self.dv = (dt*force/self.m)
        self.v = self.v+self.dv
    def updateOM(self,dt):
        if self.rigidlink and not self.updated:
            '''Si lien rigid, c'est un solide
            Evolution calculée pour UNE masse à chaque bout de la tige et pas plus
            TODO: généralisation... '''
            x1 = self.rigidlink.mass1.OM
            x2 = self.rigidlink.mass2.OM
            m1 = self.rigidlink.mass1.m
            m2 = self.rigidlink.mass2.m
            mT = m1+m2
            xG = m1*x1/mT+m2*x2/mT
            m1dv1 = m1*self.rigidlink.mass1.dv
            m2dv2 = m2*self.rigidlink.mass2.dv
            # Calcul de la nouvelle vG
            self.rigidlink.vG += m1dv1/mT+m2dv2/mT
            # calcul du nouveau omega
            GM1 = x1-xG
            GM2 = x2-xG
            self.rigidlink.w += (GM1.cross(m1dv1)+GM2.cross(m2dv2)) / \
                (m1*norm(GM1)**2+m2*norm(GM2)**2)
            # Calcul des vitesses v1 et v2
            self.rigidlink.mass1.v = self.rigidlink.vG - \
                pygame.math.Vector2(GM1[1]*self.rigidlink.w, -GM1[0]*self.rigidlink.w)
            self.rigidlink.mass2.v = self.rigidlink.vG - \
                pygame.math.Vector2(GM2[1]*self.rigidlink.w, -GM2[0]*self.rigidlink.w)

        # Mise à jour de position une fois les 'bonnes vitesses' calculées si besoin
        if not self.updated:
            self.OM = self.OM+dt*self.v

        # Si on a une tige il ne faut pas qu'lle change de taille.
        if self.rigidlink and not self.updated:
            taille = norm(x2-x1)
            # Ce qu'il y a à enlever est réparti entre les deux masses prop à la masse de l'autre
            u = pygame.math.Vector2.normalize(x2-x1)  # uM1M2
            self.rigidlink.mass1.OM = x1+(m2*(taille-self.rigidlink.length)/mT)*u
            self.rigidlink.mass2.OM = x2-(m1*(taille-self.rigidlink.length)/mT)*u
            self.rigidlink.mass1.updated=True
            self.rigidlink.mass2.updated=True

    def draw(self, screen):
        if self.visible:
            self.form.screen=screen
            self.form.draw()
