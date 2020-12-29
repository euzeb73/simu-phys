# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:26:03 2020

@author: jimen
"""

import pygame
import numpy as np
from mass import Mass
from links import LinkCsteF
from functions import norm
import values

class World():
    def __init__(self,sizex,sizey):
        
        
        '''Ajouter un restart'''
        
        self.sizex=sizex #Taille du monde en m. le mieux c'est de respecter sizex=4/3 sizey
        self.sizey=sizey
        self.rect=pygame.Rect(0,0,values.WIDTH,values.HEIGHT) #le rectangle monde par défaut
        self.mass=[]
        self.link=[]
        self.g=9.81
        self.vecg=np.array([0,-self.g])
        self.color=(255,255,255)
        self.screen=0 #Il faudra mettre la surface pygame dans laquelle on affiche
        self.dt=0.1
        self.gravity=True
        self.earth=Mass(1e24)
        self.earth.visible=False
        
    def add_Mass(self,m):
        '''Ajoute la masse et les liens qui lui sont associés au monde'''
        self.mass.append(m)
        if self.gravity:
            lien=LinkCsteF(m,self.earth,[0,-m.m*self.g]) 
            self.add_Link(lien)
        for link,num in m.linklist:
            if link not in self.link:
                self.link.append(link)
    def add_Link(self,l):
        ''' A n'utiliser que si on a ajouté des masses sans liens
        Utiliser add mass qui ajoute aussi les liens'''
        self.link.append(l)
    
    def enable_gravity(self,g):
        '''Si on active la gravité après avoir ajouté des masses
        pas utile normalement'''
        for mass in self.mass:
            lien=LinkCsteF(mass,self.earth,[0,-mass.m*self.g]) 
            self.add_Link(lien)
            
    def disable_gravity(self,masslist=[]):
        '''Desactive la gravité pour les mass de masslist
        ou pour toutes les masses si masslist est vide'''
        if masslist==[]:
            masslist=self.mass
        for mass in masslist:
            for i in range(len(mass.linklist)):
                lien,num=mass.linklist[i]
                if num==1:
                    if lien.mass2==self.earth:
                        del mass.linklist[i]
                        self.link.remove(lien)
                else:
                    if lien.mass1==self.earth:
                        del mass.linklist[i]
                        self.link.remove(lien)
                        
    def update(self):
        #Mise à jour des positions des masses
        for mass in self.mass:
            #somme des forces
            force=pygame.math.Vector2(0,0)
            for link,num in mass.linklist:
                if not link.rigid:
                    if num==1:
                        force+=link.force1
                    elif num==2:
                        force+=link.force2
#            for link,num in mass.linklist:
#                if link.rigid:
#                    x1=link.mass1.OM
#                    x2=link.mass2.OM
#                    u=(x1-x2)/norm(x1-x2)
#                    deltaf=np.dot(force,u)*u
#                    if num==1:
#                        force=force+deltaf
#                    elif num==2:
#                        force=force-deltaf
            mass.dv=(self.dt*force/mass.m)
            mass.v=mass.v+mass.dv
            
        for link in self.link:
#            print('v avant {}'.format(mass.v))
            if link.rigid:
                '''Si lien rigid, c'est un solide
                Evolution calculée pour UNE masse à chaque bout de la tige et pas plus
                TODO: généralisation... '''
                x1=link.mass1.OM
                x2=link.mass2.OM
                m1=link.mass1.m
                m2=link.mass2.m
                mT=m1+m2
                xG=m1*x1/mT+m2*x2/mT
                m1dv1=m1*link.mass1.dv
                m2dv2=m2*link.mass2.dv
                #Calcul de la nouvelle vG
                link.vG+=m1dv1/mT+m2dv2/mT
                #calcul du nouveau omega
                GM1=x1-xG
                GM2=x2-xG
                link.w+=(GM1.cross(m1dv1)+GM2.cross(m2dv2))/(m1*norm(GM1)**2+m2*norm(GM2)**2)
                #Calcul des vitesses v1 et v2
                link.mass1.v=link.vG-pygame.math.Vector2(GM1[1]*link.w,-GM1[0]*link.w)
                link.mass2.v=link.vG-pygame.math.Vector2(GM2[1]*link.w,-GM2[0]*link.w)
        
        #Mise à jour des positions une fois les 'bonnes vitesses' calculées
        for mass in self.mass:
            mass.OM=mass.OM+self.dt*mass.v
            
        #Mise à jour des forces: recalculées avec les positions
        for link in self.link:
            if not link.rigid: #☻inutile d'update les rigids
                link.update()
                
    def draw(self):
        pygame.draw.rect(self.screen,(255,255,255),self.rect)
        for l in self.link:
            l.draw(self.screen)
        for m in self.mass:
            m.draw(self.screen)
