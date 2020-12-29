# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from libfiles.mass import Mass
from libfiles.links import LinkCsteF,LinkRigid,LinkSpring
from libfiles.world import World
from libfiles.app import App
import libfiles.values


k=10
l0=1

monde=World(3,3)
mfixe=Mass(1e6,[1.5,2])
mfixe.visible=False
mfixe2=Mass(1e6,[1.5,2.5])
mfixe2.visible=False
m=Mass(1,[2.5,2])
ressort=LinkSpring(m,mfixe2,k,l0)
tige=LinkRigid(m,mfixe)
monde.add_Mass(m)
monde.add_Mass(mfixe)
monde.add_Mass(mfixe2)
monde.disable_gravity([mfixe,mfixe2])
appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()