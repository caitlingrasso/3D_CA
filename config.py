import numpy as np

import constants as c
from visualizations import display_grid

center = c.GRID_SIZE // 2
third = c.GRID_SIZE // 3
quarter = c.GRID_SIZE // 4
eighth = c.GRID_SIZE // 8

# ------------------------------------------------
# INITIAL CELL CONDITIONS
# ------------------------------------------------

def shape_generation(option):
    cells = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    if option == 'single_cell':
        cells[center, center, center] = 1
    elif option == 'cube':
        cells[third:c.GRID_SIZE-third, third:c.GRID_SIZE-third, third:c.GRID_SIZE-third] = 1
    return cells

# ------------------------------------------------
# INITIAL VOLTAGE CONDITIONS
# ------------------------------------------------

def set_pacemaker():
    # initial voltage grid = voltage starts at 255 in center cell
    volt = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    volt[center, center, center] = 255
    # volt[center+1, center, center] = 100
    return volt




