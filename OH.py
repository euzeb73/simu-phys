# -*- coding: utf-8 -*-

from simphys.mass import Mass
from simphys.links import LinkCsteF, LinkRigid, LinkSpring
from simphys.world import World
from simphys.app import App

k = 40

l0 = 1

monde = World(3, 3)
mfixe2 = Mass(1e10, [1.5, 2.5])
mfixe2.form.visible = False
m = Mass(1, [1.5, 1.5])
ressort = LinkSpring(m, mfixe2, k, l0)
monde.add_Mass(m)
monde.add_Mass(mfixe2)
monde.disable_gravity([mfixe2])
appli = App()
appli.add_World(monde)
appli.set_speed(0.125)
appli.run()
quit()