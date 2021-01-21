# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:24:53 2020

@author: jimen
"""
import pygame

from .forms import Circle, Square, Polygone
from .functions import norm
from math import sqrt

class Mass():
    def __init__(self, m=1, OM=[0, 0], angle=0, v=[0, 0], w=0, form='Circle'):
        self.m0 = m
        self.OM0 = pygame.math.Vector2(OM[0], OM[1])
        self.v0 = pygame.math.Vector2(v[0], v[1])
        self.w0 = w
        self.angle = angle
        self.size=0.1
        self.rigidlink=None
        self.updated=False #pour voir si on a mis à jour la masse ou pas
        self.linklist = []
        self.collides = True
        if form == 'Circle':
            self.form = Circle(self)
        elif form == 'Square':
            self.form = Square(self)
        self.restart()

    def set_size(self,size):
        self.size=size
        self.form.size=size

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

        if self.rigidlink and self.updated:
            #la masse est reliée à une tige et c'est la deuxième à etre mise à jour
            self.v-=self.dv #on annule la modif de vitesse due aux forces ce qui redonne la vitesse calculée par le mouvement de la tige

        # Mise à jour de position une fois les 'bonnes vitesses' calculées si besoin       
        self.OM = self.OM+dt*self.v
        
        # Si on a une tige il ne faut pas qu'elle change de taille.
        if self.rigidlink and not self.updated:
            x1 = self.rigidlink.mass1.OM
            x2 = self.rigidlink.mass2.OM
            taille = norm(x2-x1)
            # Ce qu'il y a à enlever est réparti entre les deux masses prop à la masse de l'autre
            u = pygame.math.Vector2.normalize(x2-x1)  # uM1M2
            self.rigidlink.mass1.OM = x1+(m2*(taille-self.rigidlink.length)/mT)*u
            self.rigidlink.mass2.OM = x2-(m1*(taille-self.rigidlink.length)/mT)*u
            self.rigidlink.mass1.updated=True
            self.rigidlink.mass2.updated=True

    def detect_bounce(self,world,dt):
        '''dt pour remonter les positions d'un cran: avant que ça se touche'''
        '''TODO faire un bon calcul des positions corrigées
        (pas que corriger une coordonnée)'''
        limite=world.sizex-self.size
        x0=self.OM[0]-self.v[0]*dt
        y0=self.OM[1]-self.v[1]*dt
        if self.OM[0]>limite:
            self.OM[0]=limite
            self.OM[1]=y0+self.v[1]*(limite-x0)/self.v[0]
            self.v[0]=-self.v[0]
        limite=self.size
        if self.OM[0]<limite:
            self.OM[0]=limite
            self.OM[1]=y0+self.v[1]*(limite-x0)/self.v[0]
            self.v[0]=-self.v[0]
        limite=world.sizey-self.size
        if self.OM[1]>limite:
            self.OM[0]=x0+self.v[0]*(limite-y0)/self.v[1]
            self.OM[1]=limite
            self.v[1]=-self.v[1]
        limite=self.size
        if self.OM[1]<limite:
            self.OM[0]=x0+self.v[0]*(limite-y0)/self.v[1]
            self.OM[1]=limite
            self.v[1]=-self.v[1]

    def handle_collision(self,mass,dt):
        '''dt pour remonter les positions d'un cran: avant que ça se touche'''
        collision=self.detect_collision(mass)
        if collision:
            #on change les vitesses
            # https://physics.stackexchange.com/questions/107648/what-are-the-general-solutions-to-a-hard-sphere-collision
            #permet de faire les calculs avec les 3 conservartions
            # en fait la conservation du moment cinétique amène celle de l'impulsion que la diff de vitesse pour
            # les masses est colinéaire à l'axe passant par les centres des boules.
            #Après on exprime les nvelles vitesse avec les ancienne+- la même d'impulsion divisée par masse
            #dans la conservation de l'EC ça donne le résultat utilisé.
            x10=self.OM-self.v*dt
            x20=mass.OM-mass.v*dt
            M2M10=x10-x20
            dmin=self.size+mass.size
            v1=self.v
            v2=mass.v
            dv=v2-v1
            deltat=-(M2M10.dot(dv)+sqrt((M2M10.dot(dv))**2-dv.dot(dv)*(M2M10.dot(M2M10)-dmin**2)))/dv.dot(dv)
            x1=x10+v1*deltat
            x2=x20+v2*deltat
            m1=self.m
            m2=mass.m
            M2M1=x1-x2
            if M2M1.length()>0:
                n=M2M1.normalize()
                P=2*(n.dot(v2-v1)/(1/m1+1/m2))*n  #Variation d'impulsion
                self.v+=P/m1
                mass.v-=P/m2

    def detect_collision(self,mass):
        collision=False
        d=norm(self.OM-mass.OM)
        if d<=self.size+mass.size:
            collision=True
            print('collision')
        return collision


    def draw(self, screen):
        self.form.draw(screen)
