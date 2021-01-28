# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:16:59 2020

@author: jimen
"""

import numpy as np
import pygame
from .functions import norm
from .linksforms import LinkForm,SpringForm

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

        super().__init__(m1, m2)
        self.linkForm.visible=True
        self.rigid = True
        self.length = norm(self.mass1.OM-self.mass2.OM)
        self.mass1.rigidlink=self
        self.mass2.rigidlink=self
        self.correctCI() #pour réajuster les vitesses si pas compatibes avec tige rigide
        self.update()

    def correctCI(self):
        '''Recalcule vG et omega à partir de v1 et v2
        elimine les problèmes dans les vitesses '''
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
        x1 = self.mass1.OM
        x2 = self.mass2.OM
        v1 = self.mass1.v
        v2 = self.mass2.v
        m1=self.mass1.m
        m2=self.mass2.m
        F1=pygame.math.Vector2([0,0])
        for link,num in self.mass1.linklist:
            if link is not self:
                if num == 1:
                    F1+= link.force1
                elif num == 2:
                    F1+= link.force2
        F2=pygame.math.Vector2([0,0])
        for link,num in self.mass2.linklist:
            if link is not self:
                if num == 1:
                    F2+= link.force1
                elif num == 2:
                    F2+= link.force2
        l = norm(x1-x2)
        uM1M2 = pygame.math.Vector2.normalize(x2-x1)
        mu=(m1*m2)/(m1+m2)
        T=uM1M2*mu*((v2-v1).dot(v2-v1)+(x2-x1).dot(F2/m2-F1/m1))/l
        self.force1=T
        self.force2=-T


class LinkCsteF(Link):
    def __init__(self, m1, m2, F):
        '''Lien avec force constante'''
        self.force1 = np.array(F)
        self.force2 = -self.force1
        super().__init__(m1, m2)
        self.rigid = False


class LinkSpring(Link):
    def __init__(self, m1, m2, k, l0):
        '''Lien avec ressort'''
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