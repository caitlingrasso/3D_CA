import numpy as np
import constants as c
from ca import CA
from config import sphere, cube

sphere = sphere()
filename = 'sphere{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.refractory_time, c.pulse_time, c.CA_ITER)

ca = CA(sphere)
ca.run(save=True, fn=filename)

cube = cube()
filename = 'cube{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.refractory_time, c.pulse_time, c.CA_ITER)

ca = CA(cube)
ca.run(save=True, fn=filename)

