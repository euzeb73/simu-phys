# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from simphys.mass import Mass
from simphys.links import LinkCsteF, LinkRigid, LinkSpring
from simphys.world import World
from simphys.app import App


g = 9.81


monde = World(10, 10)
# m1=Mass(0.01,[6,6.5])
# m2=Mass(0.01,[5,5])
m2 = Mass(1, [6.5, 5])
m3 = Mass(1, [6.5, 4])
m4 = Mass(1, [7, 4], 0, [-10, 0])
m4.form.color = (0, 128, 255)
# t12=LinkRigid(m1,m2)
t23 = LinkRigid(m2, m3)
# t31=LinkRigid(m3,m1)
# monde.add_Mass(m1)
monde.add_Mass(m2)
monde.add_Mass(m3)
monde.add_Mass(m4)

monde.save_state()
newworld = World()
newworld.load_dico(monde.dico)
appli = App()
appli.add_World(newworld)
appli.set_speed(0.125)
appli.run()
