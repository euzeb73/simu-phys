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


taillex=2
tailley=1
monde=World(taillex,tailley)
rayon=0.1
pt1=Mass(1e20,[0.5,0.9])
pt1.form.visible=False
pt1.collides=False
m1=Mass(1,[0.5,0.3])
m1.set_size(rayon)
pt2=Mass(1e20,[0.71,0.9])
pt2.form.visible=False
pt2.collides=False
m2=Mass(1,[0.71,0.3])
m2.set_size(rayon)
pt3=Mass(1e20,[0.92,0.9])
pt3.form.visible=False
pt3.collides=False
m3=Mass(1,[0.92,0.3])
m3.set_size(rayon)
pt4=Mass(1e20,[1.13,0.9])
pt4.form.visible=False
pt4.collides=False
m4=Mass(1,[1.73,0.9])
m4.set_size(rayon)
l1=LinkRigid(pt1,m1)
l2=LinkRigid(pt2,m2)
l3=LinkRigid(pt3,m3)
l4=LinkRigid(pt4,m4)

monde.add_Mass(m4)
monde.add_Mass(m1)
monde.add_Mass(m2)
monde.add_Mass(m3)

monde.add_Mass(pt1)
monde.add_Mass(pt2)
monde.add_Mass(pt3)
monde.add_Mass(pt4)
monde.disable_gravity([pt1,pt2,pt3,pt4])

appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()