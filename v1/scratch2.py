import numpy as np
import time

from config import shape_generation2, set_pacemaker
# from visualizations import plot_body_and_voltage, plot_voxels
from ca import CA
import constants as c

start_time = time.time()

c.GRID_SIZE = 21
c.a = 0.9 # makes signal last in cells longer when higher
c.b = 10  # propagates signal faster when higher
c.CA_ITER = 1000

shape = 'sphere'
body, voltage = shape_generation2(shape)

ca = CA(body, voltage)
filename = shape + '{}_{}iter_a{}_b{}_pulse.mp4'.format(c.GRID_SIZE,c.CA_ITER,c.a,c.b)
ca.run2(save=True, iterations=c.CA_ITER, fn=filename)

end_time = time.time()
print((end_time-start_time)/60)  # minutes


