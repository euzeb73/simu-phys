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

g=9.81        

n=10
k=100 #raideur en Nm^-1

monde=World(0.5+0.25*n,1)
monde.gravity=False

#Chaine libre
masslist=[]
for i in range(n):
    if i==0:
        m=Mass(1,[0.25,0.7])
        m.form.R=0.05
    else:
        m=Mass(1,[0.5+0.25*i,0.7])
        m.form.R=0.05
    masslist.append(m)

for i in range(n-1):
    l=LinkSpring(masslist[i],masslist[i+1],k,0.25)

for mass in masslist:
    monde.add_Mass(mass)

#Extremité fixe
masslist=[]
for i in range(n):
    if i==0:
        m=Mass(1,[0.25,0.3])
        m.form.R=0.05
    else:
        m=Mass(1,[0.5+0.25*i,0.3])
        m.form.R=0.05
    masslist.append(m)

masslist[-1].m=1e6
for i in range(n-1):
    l=LinkSpring(masslist[i],masslist[i+1],k,0.25)

for mass in masslist:
    monde.add_Mass(mass)
    
appli=App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()