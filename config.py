import numpy as np
import copy

import constants as c
from visualizations import plot_voxels, plot_body_and_voltage

def shape_generation(option):
    if option == 'cube':
        body = np.ones((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    elif option == 'sphere':
        body = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        length = c.GRID_SIZE
        radius = int((length - 1) / 2)
        r2 = np.arange(-radius, radius + 1) ** 2
        dist2 = r2[:, None, None] + r2[:, None] + r2
        body[dist2 <= radius ** 2] = 2
        body[0, :, :] = 0
        body[length - 1, :, :] = 0
        body[:, 0, :] = 0
        body[:, length - 1, :] = 0
        body[:, :, 0] = 0
        body[:, :, length - 1] = 0
        voltage = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        voltage[radius,radius,radius] = 500
    return body

def shape_generation2(option):
    cells = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    if option == 'cube':
        body = np.ones((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        center = c.GRID_SIZE // 2
        voltage = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        voltage[center, center, center] = 500
    elif option == 'sphere':
        body = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        length = c.GRID_SIZE
        radius = int((length - 1) / 2)
        r2 = np.arange(-radius, radius + 1) ** 2
        dist2 = r2[:, None, None] + r2[:, None] + r2
        body[dist2 <= radius ** 2] = 2
        body[0, :, :] = 0
        body[length - 1, :, :] = 0
        body[:, 0, :] = 0
        body[:, length - 1, :] = 0
        body[:, :, 0] = 0
        body[:, :, length - 1] = 0
        voltage = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
        voltage[radius,radius,radius] = 500
    return body, voltage

def set_pacemaker(): # pass in body and choose random number where body == 1
    # initial voltage grid = voltage starts at 255 in center cell
    center = c.GRID_SIZE//2
    volt = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    volt[center, center, center] = 500
    return volt


