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
        self.earth.collides=False
        self.boucingbounds=True #(bords rebondissants)
        self.rigidsnb=0

    def prepare(self):
        '''fait un dictionnaire pour les liens rigides
        avec en keys les 2 masses et en values
        le num dans la list '''
        i=0
        self.rigidsdict=dict()
        for link in self.link:
            if link.rigid:
                m1=link.mass1
                m2=link.mass2
                i1=self.mass.index(m1)
                i2=self.mass.index(m2)
                self.rigidsdict[(min(i1,i2),max(i1,i2))]=i #Toujours i<j
                i+=1



    
    def restart(self):
        for mass in self.mass:
            mass.restart()
        self.update_rigids() #il faut réinitialiser les forces des liens rigid
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
                self.add_Link(link)

    def add_Link(self, l):
        ''' A n'utiliser que si on a ajouté des masses sans liens
        Utiliser add mass qui ajoute aussi les liens'''
        if l.rigid:
            self.rigidsnb+=1
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
    def detect_wall_bounce(self):
        for mass in self.mass:
            mass.detect_bounce(self,self.dt)

    def detect_bounce(self):
        #On fait le bilan 2 à 2 des collisions des masses
        for i in range(len(self.mass)-1):
            if self.mass[i].collides:
                for j in range(i+1,len(self.mass)):
                    if self.mass[j].collides:
                        self.mass[i].handle_collision(self.mass[j],self.dt)

    def calc_rigids(self):
        '''Calcule les forces des liens rigides'''
        systmatrixA=np.zeros((self.rigidsnb,self.rigidsnb)) #Système A X= B avec X=les forces qu'on cherche
        systB=np.zeros(self.rigidsnb)
        ligne=0
        for link in self.link:
            if link.rigid:
                m1=link.mass1
                m2=link.mass2
                i1=self.mass.index(m1)
                i2=self.mass.index(m2)
                v1=m1.v
                v2=m2.v
                M1M2=m2.OM-m1.OM
                F1=m1.sumforces(True) #la somme des forces sans les liens rigides
                F2=m2.sumforces(True)
                systB[ligne]=(v2-v1).dot(v2-v1)+M1M2.dot(F2/m2.m-F1/m1.m)
                for l,num in m1.linklist:
                    if l.rigid:
                        if num==1:
                            mj=l.mass2
                        else:
                            mj=l.mass1
                        M1Mj=mj.OM-m1.OM
                        j=self.mass.index(mj)
                        if i1<j: #Pour les liens on a choisi i<j
                            epsilon=1
                        else: #si i>j c'est la force opposée
                            epsilon=-1
                        colonne=self.rigidsdict[(min(i1,j),max(i1,j))]
                        systmatrixA[ligne,colonne]=epsilon*M1M2.dot(M1Mj)/(m1.m*M1Mj.length())
                for l,num in m2.linklist:
                    if l.rigid:
                        if num==1:
                            ml=l.mass2
                        else:
                            ml=l.mass1
                        M2Ml=ml.OM-m2.OM
                        l=self.mass.index(ml)
                        if i2<l: #Pour les liens on a choisi i<j
                            epsilon=1
                        else: #si i>j c'est la force opposée
                            epsilon=-1
                        colonne=self.rigidsdict[(min(i2,l),max(i2,l))]
                        systmatrixA[ligne,colonne]+=epsilon*M1M2.dot(M2Ml)/(m2.m*M2Ml.length())
                ligne+=1
        return np.linalg.solve(systmatrixA,systB) #On trouve les valeurs des liens.

    def update_rigids(self):
        '''calcule puis mets à jours les forces des liens rigides'''
        forces=self.calc_rigids()
        i=0
        for link in self.link:
            if link.rigid:
                m1=link.mass1
                m2=link.mass2
                i1=self.mass.index(m1)
                i2=self.mass.index(m2)
                if i1<i2:
                    epsilon=1
                else:
                    epsilon=-1
                u12=pygame.math.Vector2.normalize(m2.OM-m1.OM)
                link.force1=epsilon*forces[i]*u12
                link.force2=-link.force1
                i+=1

    
    def update(self):
        # Mise à jour des positions des masses
        for mass in self.mass:
            mass.updated=False #parce qu'on n'a pas encore updated la position
            mass.updatev(self.dt)
        for mass in self.mass:
            mass.updateOM(self.dt)

        #tests de collisions entre particules
        self.detect_bounce()

        #test collision des bords:
        if self.boucingbounds:
            self.detect_wall_bounce()
        
        self.update_rigids()

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
