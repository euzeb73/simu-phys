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



monde=World(10,10)
mfixe=Mass(1e6,[5,6.5])
mfixe.visible=False
m=Mass(1,[6,6.5])
tige=LinkRigid(m,mfixe)
monde.add_Mass(m)
monde.add_Mass(mfixe)
monde.disable_gravity([mfixe])
appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()