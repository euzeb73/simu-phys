# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from mass import Mass
from links import LinkCsteF,LinkRigid,LinkSpring
from world import World
from app import App
import values

g=9.81        

m1=Mass(1,[3.5,5],0,[-5,0])
m1.form.R=0.05

m2=Mass(2,[3,6],0,[0,0])
m2.form.R=0.1
m2.form.color=(40,128,50)

m3=Mass(3,[4,6],0,[0,0])
m3.form.R=0.1
m3.form.color=(255,0,128)


l1=LinkSpring(m2,m3,500,0.8)
l2=LinkRigid(m1,m2)
l3=LinkRigid(m1,m3)


monde=World(6,7)
monde.add_Mass(m1)
monde.add_Mass(m2)
monde.add_Mass(m3)


appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
