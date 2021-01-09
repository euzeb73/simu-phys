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
mfixe=Mass(1e20,[5,6.5])
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