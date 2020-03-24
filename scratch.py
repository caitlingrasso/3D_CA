import numpy as np

from config import shape_generation, set_pacemaker
from visualizations import display_grid, plot_cells_and_signal
from ca import CA


cells = shape_generation('cube')
voltage = set_pacemaker()

# plot_cells_and_signal(cells, voltage)

ca = CA(cells, voltage)

ca.run_and_save(fn='3d_cube.mp4', iterations=50)