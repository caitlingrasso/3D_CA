import constants as c
from ca import CA
from config import sphere, cube

sphere = sphere()
filename = 'sphere{}_MS{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.max_signal, c.refactory_time, c.pulse_time, c.CA_ITER)

ca = CA(sphere)
ca.run(save=True, fn=filename)

cube = cube()
filename = 'cube{}_MS{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.max_signal, c.refactory_time, c.pulse_time, c.CA_ITER)

ca = CA(cube)
ca.run(save=True, fn=filename)

