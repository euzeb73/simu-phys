# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:16:59 2020

@author: jimen
"""

import numpy as np
import pygame
from .functions import norm


class Link():
    def __init__(self, m1, m2):
        '''Lien rigide'''
        self.visible = True
        self.color = (0, 0, 0)  # noir par défaut
        # largeur par défaut (affchage) mettre un entier impair SVP
        self.width = 3
        self.mass1 = m1
        self.mass2 = m2
        # donne le lien et le numero de la masse pour ce lien
        self.mass1.linklist.append((self, 1))
        self.mass2.linklist.append((self, 2))
        self.rigid = False
        self.update()

    def update(self):
        pass

    def draw(self, screen):
        if self.visible:
            start = OMtopx(self.mass1.OM)
            stop = OMtopx(self.mass2.OM)
            pygame.draw.line(screen, self.color, start, stop, self.width)


class LinkRigid(Link):
    def __init__(self, m1, m2):
        ''' Classe écrite pour UNE masse à chaque bout de la tige et pas plus
        TODO: généralisation... '''

        super().__init__(m1, m2)
        self.rigid = True
        self.length = norm(self.mass1.OM-self.mass2.OM)

    def update(self):
        '''Recalcule vG et omega à partir de v1 et v2
        elimine les problèmes'''
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


class LinkCsteF(Link):
    def __init__(self, m1, m2, F):
        '''Lien avec force constante'''
        self.force1 = np.array(F)
        self.force2 = -self.force1
        super().__init__(m1, m2)
        self.rigid = False
        self.visible = False


class LinkSpring(Link):
    def __init__(self, m1, m2, k, l0):
        '''Lien avec ressort'''
        self.k = k
        self.l0 = l0
        super().__init__(m1, m2)
        self.rigid = False

    def update(self):
        x1 = self.mass1.OM
        x2 = self.mass2.OM
        l = norm(x1-x2)
        # vecteur unitaire direction sens M2M1
        uM2M1 = pygame.math.Vector2.normalize(x1-x2)
        self.force1 = -self.k*(l-self.l0)*uM2M1  # force sur la masse 1
        self.force2 = -self.force1  # Newton

    def draw(self, screen):
        '''Dessine un ressort'''
        if self.visible:
            ltot = 2.1*self.l0  # Longueur du ressort entièrement détendu
            nseg = 20  # nb de segments PAIR SVP
            lseg = ltot/nseg  # Longueur d'un segment
            x1 = self.mass1.OM
            x2 = self.mass2.OM
            M1M2 = x2-x1
            l = norm(M1M2)  # longueur entre les 2 masses
            theta = np.arctan2(M1M2[1], M1M2[0])
            if l > ltot:
                alpha = 0  # ça ne devrait pas arriver
            else:
                alpha = np.arccos(l/ltot)  # Angle des segments
            depart = OMtopx(self.mass1.OM)
            liste_points = [depart]
            for i in range(0, nseg):
                if i == 0:
                    pointenm = self.mass1.OM+0.5*lseg * \
                        np.array([np.cos(alpha+theta), np.sin(theta+alpha)])
                elif i % 2 == 0:
                    pointenm = pointenm+lseg * \
                        np.array([np.cos(alpha+theta), np.sin(alpha+theta)])
                else:
                    pointenm = pointenm+lseg * \
                        np.array([np.cos(theta-alpha), np.sin(theta-alpha)])
                point = OMtopx(pointenm)
                liste_points.append(point)
            arrivee = OMtopx(self.mass2.OM)
            liste_points.append(arrivee)
            pygame.draw.lines(screen, self.color, False,
                              liste_points, self.width)
