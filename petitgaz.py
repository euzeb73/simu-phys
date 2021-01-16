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

g=9.81        
random.seed()
N=100
taillex=1
tailley=1
monde=World(taillex,tailley)
rayon=0.01
for i in range(N):
    angle=random.uniform(0,2*pi)
    norme=random.gauss(0,5)
    x=random.uniform(rayon,taillex-rayon)
    y=random.uniform(rayon,tailley-rayon)
    vx=norme*cos(angle)
    vy=norme*sin(angle)
    m=Mass(1,[x,y],0,[vx,vy])
    m.set_size(rayon)
    randcolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    m.form.color=randcolor
    monde.add_Mass(m)


appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()