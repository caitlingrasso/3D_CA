import constants as c
from ca import CA
from config import sphere, cube

# cube = cube()
# filename = 'cube{}_MS{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.max_signal, c.refactory_time, c.pulse_time, c.CA_ITER)

sphere = sphere()
filename = 'sphere{}_MS{}_RT{}_PT{}_iter{}.mp4'.format(c.GRID_SIZE, c.max_signal, c.refactory_time, c.pulse_time, c.CA_ITER)

print(sphere)
exit()

ca = CA(sphere)
ca.run(save=True, fn=filename)
