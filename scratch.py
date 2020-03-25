import numpy as np

from config import shape_generation, set_pacemaker
from visualizations import display_grid, plot_cells_and_signal
from ca import CA
import constants as c


cells = shape_generation('cube')
voltage = set_pacemaker()

# plot_cells_and_signal(cells, voltage, transparent=True)
# exit()

c.a = 0.1  # makes signal last in cells longer when higher
c.b = 0.1  # propagates signal faster when higher

ca = CA(cells, voltage)
ca.run(save=True, iterations=50, fn='cube.mp4', transparent=False)

#TODO: Pulsing pacemaker

