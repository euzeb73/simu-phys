# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 21:07:02 2020

@author: jimen
"""

from libfiles.mass import Mass
from libfiles.links import LinkCsteF,LinkRigid,LinkSpring
from libfiles.world import World
from libfiles.app import App
from libfiles.functions import norm
import libfiles.values

g=9.81        

m1=Mass(1,[2,5])
m1.form.R=0.05

m2=Mass(2,[3,6],0,[0,-0.5])
m2.form.R=0.1
m2.form.color=(40,128,50)

m3=Mass(3,[4,6],0,[0,1.5])
m3.form.R=0.1
m3.form.color=(255,0,128)


l=LinkSpring(m1,m2,100,0.8)
dist=norm(m1.OM-m3.OM)
l=LinkSpring(m1,m3,1,dist)
dist=norm(m2.OM-m3.OM)
l=LinkRigid(m2,m3)


monde=World(6,9)
#monde.g=0.1
monde.add_Mass(m1)
monde.add_Mass(m2)
monde.add_Mass(m3)



app=App()
app.add_World(monde)
app.set_speed(0.125)
app.run()
quit()