# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:26:03 2020

@author: jimen
"""

import pygame
import numpy as np
from .mass import Mass
from .links import LinkCsteF, LinkSpring, LinkRigid
from .functions import norm


class World():
    def __init__(self, sizex=4, sizey=3):
        self.sizex = sizex  # Taille du monde en m. le mieux c'est de respecter sizex=4/3 sizey
        self.sizey = sizey
        # le rectangle monde par défaut
        self.rect = pygame.Rect(0, 0, 1024, 768)
        self.mass = []
        self.link = []
        self.g = 9.81
        self.vecg = np.array([0, -self.g])
        # self.color = (255, 255, 255) #pas utile en fait
        # self.screen = 0  # Il faudra mettre la surface pygame dans laquelle on affiche
        #                 # PAS utile en fait ?
        self.dt = 0.1
        # On ajoute la Terre
        self.gravity = True
        self.earth = Mass(1e24)
        self.earth.form.visible = False
        self.earth.collides = False
        self.mass.append(self.earth)
        self.boucingbounds = True  # (bords rebondissants)
        self.rigidsnb = 0

    def save_state(self):
        '''fait un dictionnaire avec le contenu du monde'''
        self.dico = dict()
        mass_list = []
        mass_states = []
        nmass = len(self.mass)
        # en fait mieux liste de liste car on va y mettre une liste de dico
        # Initialisation avec des listes vides
        link_mat = []
        for i in range(nmass):
            ligne = []
            for j in range(nmass):
                ligne.append([])
            link_mat.append(ligne)
        for i, mass in enumerate(self.mass):
            mass.save_state()
            mass_list.append(mass.typeinfo)
            mass_states.append(mass.state)
            for link, num in mass.linklist:
                if num == 1:
                    j = self.mass.index(link.mass2)
                    num2 = 2
                    # le num de la ligne est la masse 1 du lien
                    link_mat[i][j].append(link.dico)
                elif num == 2:
                    j = self.mass.index(link.mass1)
                    num2 = 1
                    # le num de la ligne est la masse 1 du lien
                    link_mat[j][i].append(link.dico)
                # du coup pas de répétitions
                self.mass[j].linklist.remove((link, num2))
                # dans la matrice il y a uniquement une fois un lien et il est entre la masse 1
                # situé ligne i et la masse 2 située colonne j
                # il n'apparait pas en ligne j et colonne i (ça permet de distinguer masse 1 et masse 2)
            mass.linklist = []

        self.dico['mass'] = mass_list
        self.dico['mass_states'] = mass_states
        self.dico['links'] = link_mat
        self.dico['vecg'] = self.vecg
        self.dico['size'] = self.sizex, self.sizey
        self.dico['dt'] = self.dt
        self.dico['gravity'] = self.gravity
        self.dico['boucingbounds'] = self.boucingbounds

    def load_dico(self, dico):
        # charger le monde à partir du dico

        # Les propriétés générales
        self.vecg = dico['vecg']
        self.sizex, self.sizey = dico['size']
        self.dt = dico['dt']
        self.gravity = dico['gravity']
        self.boucingbounds = dico['boucingbounds']

        # On construit les masses
        self.mass = []
        for i, masstype in enumerate(dico['mass']):
            massstate = dico['mass_states'][i]
            mass = Mass()
            mass.load_mass(masstype, massstate)
            self.mass.append(mass)

        # On construit les liens
        self.link = []
        linkmat = dico['links']  # la matrice des liens
        for i in range(len(linkmat)):
            for j in range(len(linkmat)):
                # contient une liste de dico de liens entre masse i et masse j
                links = linkmat[i][j]
                masse1 = self.mass[i]
                masse2 = self.mass[j]
                for linkdic in links:
                    typ = linkdic['type']
                    lien = typ(masse1, masse2)
                    lien.linkForm.visible = linkdic['visible']
                    if typ == LinkCsteF:
                        lien.force1 = linkdic['force']
                        lien.force2 = -lien.force1
                    elif typ == LinkSpring:
                        lien.k = linkdic['k']
                        lien.l0 = linkdic['l0']
                    elif typ == LinkRigid:
                        lien.rigid = True
                    lien.update()
                    self.add_Link(lien)

    def load_world(self):
        # charger le monde à partir d'un fichier qui construit le dico
        pass

    def restart(self):
        for mass in self.mass:
            mass.restart()
        self.update_rigids()  # il faut réinitialiser les forces des liens rigid
        for link in self.link:
            link.update()

    def add_Mass(self, m):
        '''Ajoute la masse et les liens qui lui sont associés au monde'''
        self.mass.append(m)
        if self.gravity:
            lien = LinkCsteF(m, self.earth, [0, -m.m*self.g])
            self.add_Link(lien)
        for link, num in m.linklist:
            if link not in self.link:
                self.add_Link(link)

    def add_Link(self, l):
        ''' A n'utiliser que si on a ajouté des masses sans liens
        Utiliser add mass qui ajoute aussi les liens'''
        if l.rigid:
            self.rigidsnb += 1
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
            if mass.collides:
                mass.detect_bounce(self, self.dt)

    def detect_bounce(self):
        # On fait le bilan 2 à 2 des collisions des masses
        for i in range(len(self.mass)-1):
            if self.mass[i].collides:
                for j in range(i+1, len(self.mass)):
                    if self.mass[j].collides:
                        self.mass[i].handle_collision(self.mass[j], self.dt)

    def prepare(self):
        '''fait un dictionnaire pour les liens rigides
        avec en keys les 2 masses et en values
        le num dans la list '''
        i = 0
        self.rigidsdict = dict()
        for link in self.link:
            if link.rigid:
                m1 = link.mass1
                m2 = link.mass2
                i1 = self.mass.index(m1)
                i2 = self.mass.index(m2)
                self.rigidsdict[(min(i1, i2), max(i1, i2))] = i  # Toujours i<j
                i += 1

    def calc_rigids(self):
        '''Calcule les forces des liens rigides'''
        systmatrixA = np.zeros((self.rigidsnb, self.rigidsnb)
                               )  # Système A X= B avec X=les forces qu'on cherche
        systB = np.zeros(self.rigidsnb)
        ligne = 0
        for link in self.link:
            if link.rigid:
                m1 = link.mass1
                m2 = link.mass2
                i1 = self.mass.index(m1)
                i2 = self.mass.index(m2)
                v1 = m1.v
                v2 = m2.v
                M1M2 = m2.OM-m1.OM
                # la somme des forces sans les liens rigides
                F1 = m1.sumforces(True)
                F2 = m2.sumforces(True)
                systB[ligne] = (v2-v1).dot(v2-v1)+M1M2.dot(F2/m2.m-F1/m1.m)
                for l, num in m1.linklist:
                    if l.rigid:
                        if num == 1:
                            mj = l.mass2
                        else:
                            mj = l.mass1
                        M1Mj = mj.OM-m1.OM
                        j = self.mass.index(mj)
                        if i1 < j:  # Pour les liens on a choisi i<j
                            epsilon = 1
                        else:  # si i>j c'est la force opposée
                            epsilon = -1
                        colonne = self.rigidsdict[(min(i1, j), max(i1, j))]
                        systmatrixA[ligne, colonne] = epsilon * \
                            M1M2.dot(M1Mj)/(m1.m*M1Mj.length())
                for l, num in m2.linklist:
                    if l.rigid:
                        if num == 1:
                            ml = l.mass2
                        else:
                            ml = l.mass1
                        M2Ml = ml.OM-m2.OM
                        l = self.mass.index(ml)
                        if i2 < l:  # Pour les liens on a choisi i<j
                            epsilon = 1
                        else:  # si i>j c'est la force opposée
                            epsilon = -1
                        colonne = self.rigidsdict[(min(i2, l), max(i2, l))]
                        systmatrixA[ligne, colonne] += epsilon * \
                            M1M2.dot(M2Ml)/(m2.m*M2Ml.length())
                ligne += 1
        # On trouve les valeurs des liens.
        return np.linalg.solve(systmatrixA, systB)

    def update_rigids(self):
        '''calcule puis mets à jours les forces des liens rigides'''
        forces = self.calc_rigids()
        i = 0
        for link in self.link:
            if link.rigid:
                m1 = link.mass1
                m2 = link.mass2
                i1 = self.mass.index(m1)
                i2 = self.mass.index(m2)
                if i1 < i2:
                    epsilon = 1
                else:
                    epsilon = -1
                u12 = pygame.math.Vector2.normalize(m2.OM-m1.OM)
                link.force1 = epsilon*u12*forces[i]
                link.force2 = -link.force1
                i += 1

    def update(self):

        self.update_rigids()  # On commence par calculer les forces des liens rigides
        # Une vérif de calcul des forces
        T = self.link[1].force1.length()
        # Pour le pendule
        OM = self.mass[0].OM-pygame.math.Vector2((5, 6.5))
        T2 = 9.81*OM.dot(pygame.math.Vector2((0, -1))) / \
            OM.length()+self.mass[0].v.length()**2
        # print(T, T2, T-T2)

        # Mise à jour des positions des masses
        for mass in self.mass:
            mass.updatev(self.dt)
        for mass in self.mass:
            mass.updateOM(self.dt)

        # tests de collisions entre particules
        self.detect_bounce()

        # test collision des bords:
        if self.boucingbounds:
            self.detect_wall_bounce()

        # Mise à jour des forces dans les liens
        for link in self.link:
            link.update()

    def draw(self, screen):
        window = screen.window
        pygame.draw.rect(window, (255, 255, 255), screen.worldrect)
        for l in self.link:
            l.draw(screen)
        for m in self.mass:
            m.draw(screen)
