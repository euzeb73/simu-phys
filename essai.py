# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from simphys.mass import Mass
from simphys.links import LinkCsteF,LinkRigid,LinkSpring
from simphys.world import World
from simphys.app import App


g=9.81        


monde=World(10,10)
m1=Mass(1,[6,6.5])
m2=Mass(5,[5,5])
m3=Mass(0.1,[6.5,4])
t12=LinkRigid(m1,m2)
t23=LinkRigid(m2,m3)
t31=LinkRigid(m3,m1)
monde.add_Mass(m1)
monde.add_Mass(m2)
monde.add_Mass(m3)
appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
