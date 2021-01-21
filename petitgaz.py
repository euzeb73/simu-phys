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

g=9.81        
random.seed()
N=200
taillex=1
tailley=1
monde=World(taillex,tailley)
rayon=0.01

def check_collision(world,mass):
    collision=False
    for m in world.mass:
        if m is not mass:
            if m.detect_collision(mass):
                collision=True
    return collision

#Masses identiques
# for i in range(N):
#     angle=random.uniform(0,2*pi)
#     norme=random.gauss(0,0.1)
#     x=random.uniform(rayon,taillex-rayon)
#     y=random.uniform(rayon,tailley-rayon)
#     vx=norme*cos(angle)
#     vy=norme*sin(angle)
#     m=Mass(1,[x,y],0,[vx,vy])
#     m.set_size(rayon)
#     randcolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
#     m.form.color=randcolor
#     monde.add_Mass(m)

#Masses différentes
for i in range(N):
    angle=random.uniform(0,2*pi)
    norme=random.gauss(0,0.1)
    x=random.uniform(rayon,taillex-rayon)
    y=random.uniform(rayon,tailley-rayon)
    vx=norme*cos(angle)
    vy=norme*sin(angle)
    mass=random.gauss(5,2)
    if mass<1e-3:
        mass=1e-3 #mass minimale
    m=Mass(1,[x,y],0,[vx,vy])
    m.set_size(rayon*(mass)**(0.33))
    randcolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    m.form.color=randcolor
    while check_collision(monde,m):
        x=random.uniform(rayon,taillex-rayon)
        y=random.uniform(rayon,tailley-rayon)
        m.OM=pygame.math.Vector2((x,y))
    
    monde.add_Mass(m)


monde.disable_gravity()

appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()