
import pygame
import numpy as np
from .functions import norm

class LinkForm():
    def __init__(self,link,color=(0,0,0)):
        self.link=link
        self.color=color
        self.visible=False
        self.width=3

    def draw(self,screen):
        if self.visible:
            start = screen.OMtopx(self.link.mass1.OM)
            stop = screen.OMtopx(self.link.mass2.OM)
            pygame.draw.line(screen.window, self.color, start, stop, self.width)

class SpringForm(LinkForm):
    def __init__(self,link,color=(0,0,0)):
        super().__init__(link,color)
        self.ltot=2*self.link.l0
        self.nseg=20
        self.visible=True
    def draw(self,screen):
        '''Dessine un ressort'''
        if self.visible:
            ltot = self.ltot  # Longueur du ressort entièrement détendu
            nseg = self.nseg  # nb de segments PAIR SVP
            lseg = ltot/nseg  # Longueur d'un segment
            x1 = self.link.mass1.OM
            x2 = self.link.mass2.OM
            M1M2 = x2-x1
            l = norm(M1M2)  # longueur entre les 2 masses
            theta = np.arctan2(M1M2[1], M1M2[0])
            if l > ltot:
                alpha = 0  # ça ne devrait pas arriver
            else:
                alpha = np.arccos(l/ltot)  # Angle des segments
            depart = screen.OMtopx(self.link.mass1.OM)
            liste_points = [depart]
            for i in range(0, nseg):
                if i == 0:
                    pointenm = self.link.mass1.OM+0.5*lseg * \
                        np.array([np.cos(alpha+theta), np.sin(theta+alpha)])
                elif i % 2 == 0:
                    pointenm = pointenm+lseg * \
                        np.array([np.cos(alpha+theta), np.sin(alpha+theta)])
                else:
                    pointenm = pointenm+lseg * \
                        np.array([np.cos(theta-alpha), np.sin(theta-alpha)])
                point = screen.OMtopx(pointenm)
                liste_points.append(point)
            arrivee = screen.OMtopx(self.link.mass2.OM)
            liste_points.append(arrivee)
            pygame.draw.lines(screen.window, self.color, False,
                              liste_points, self.width)
