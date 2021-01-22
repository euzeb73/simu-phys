# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from simphys.mass import Mass
from simphys.links import LinkCsteF,LinkRigid,LinkSpring
from simphys.world import World
from simphys.app import App
import random
from math import cos,sin,pi
import pygame


taillex=10
tailley=5
monde=World(taillex,tailley)
rayon=0.1
N=30
L=1
anchorptlist=[]
for i in range(N):
    x=rayon+L+2*i*rayon
    pt=Mass(1e20,[x,(tailley+L)/2])
    pt.form.visible=False
    pt.collides=False
    anchorptlist.append(pt)
    if i <N-1:
        m=Mass(1,[x,(tailley+L)/2-L])
        m.set_size(rayon)
        l=LinkRigid(pt,m)
    else:        
        m=Mass(1,[x+L,(tailley+L)/2])
        m.set_size(rayon)
        l=LinkRigid(pt,m)
    monde.add_Mass(m)
    monde.add_Mass(pt)

monde.disable_gravity(anchorptlist)

monde.boucingbounds=False

appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()