# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:16:59 2020

@author: jimen
"""

import numpy as np
import pygame
from .functions import norm
from .linksforms import LinkForm,SpringForm

#######
# Linktypes
# 0 pas de lien
# 1 LinkRigid
# 10  LinkcsteF
# 100 LinkSpring
# 1000 etc...


class Link():
    def __init__(self, m1, m2):
        '''Lien de base'''
        self.mass1 = m1
        self.mass2 = m2
        # donne le lien et le numero de la masse pour ce lien
        self.mass1.linklist.append((self, 1))
        self.mass2.linklist.append((self, 2))
        self.rigid = False
        self.linkForm=LinkForm(self)
        self.update()

    def update(self):
        pass

    def draw(self, screen):
        self.linkForm.draw(screen)

class LinkRigid(Link):
    def __init__(self, m1, m2):
        ''' Classe écrite pour UNE masse à chaque bout de la tige et pas plus
        TODO: généralisation... '''
        self.linktype=1
        self.length = norm(m1.OM-m2.OM)
        self.force1=pygame.math.Vector2((0,0))
        self.force2=pygame.math.Vector2((0,0))
        super().__init__(m1, m2)
        self.linkForm.visible=True
        self.rigid = True

        self.correctCI() #pour réajuster les vitesses si pas compatibes avec tige rigide
        self.update()

    def correctCI(self):
        '''Recalcule vG et omega à partir de v1 et v2
        elimine les problèmes dans les vitesses
        TODO : Eviter ça en initialisant une fois les forces à partir des CI '''
        m1 = self.mass1.m
        m2 = self.mass2.m
        mT = m1+m2
        x1 = self.mass1.OM
        x2 = self.mass2.OM
        v1 = self.mass1.v
        v2 = self.mass2.v
        xG = m1*x1/mT+m2*x2/mT
        vG = m1*v1/mT+m2*v2/mT
        u = pygame.math.Vector2.normalize(x2-x1)  # uM1M2
        # vecteur unitaire directement orthogonal
        uortho = pygame.math.Vector2(-u[1], u[0])

        # "Corrige" les vitesses
        self.mass1.v += (-v1.dot(u)+vG.dot(u))*u
        self.mass2.v += (-v2.dot(u)+vG.dot(u))*u
        v1 = self.mass1.v
        v2 = self.mass2.v
        # Calcul de omega
        w = (v2.dot(uortho)-v1.dot(uortho))/(norm(x1-xG)+norm(x2-xG))
        # Corrige les vitesses dans l'autre direction
        self.mass1.v += (-v1.dot(uortho)+vG.dot(uortho)-norm(x1-xG)*w)*uortho
        self.mass2.v += (-v2.dot(uortho)+vG.dot(uortho)+norm(x2-xG)*w)*uortho
        v1 = self.mass1.v
        v2 = self.mass2.v
        # Recalcule vG et w
        self.vG = m1*v1/mT+m2*v2/mT
        self.w = (v2.dot(uortho)-v1.dot(uortho))/(norm(x1-xG)+norm(x2-xG))
    
    def update(self):
        pass
        #PAS trop utile apparemment, si les forces sont bien calculées
        m1 = self.mass1.m
        m2 = self.mass2.m
        mT = m1+m2
        x1 = self.mass1.OM
        x2 = self.mass2.OM
        taille = norm(x2-x1)
        # Ce qu'il y a à enlever est réparti entre les deux masses prop à la masse de l'autre
        u = pygame.math.Vector2.normalize(x2-x1)  # uM1M2
        self.mass1.OM = x1+(m2*(taille-self.length)/mT)*u
        self.mass2.OM = x2-(m1*(taille-self.length)/mT)*u

class LinkCsteF(Link):
    def __init__(self, m1, m2, F):
        '''Lien avec force constante'''
        self.linktype=10
        self.force1 = np.array(F)
        self.force2 = -self.force1
        super().__init__(m1, m2)
        self.rigid = False

class LinkSpring(Link):
    def __init__(self, m1, m2, k, l0):
        '''Lien avec ressort'''
        self.linktype=100
        self.k = k
        self.l0 = l0
        super().__init__(m1, m2)
        self.linkForm=SpringForm(self)
        self.rigid = False

    def update(self):
        x1 = self.mass1.OM
        x2 = self.mass2.OM
        l = norm(x1-x2)
        # vecteur unitaire direction sens M2M1
        uM2M1 = pygame.math.Vector2.normalize(x1-x2)
        self.force1 = -self.k*(l-self.l0)*uM2M1  # force sur la masse 1
        self.force2 = -self.force1  # Newton