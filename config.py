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

def sphere():
    body = np.zeros((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    length = c.GRID_SIZE
    radius = int((length - 1) / 2)
    r2 = np.arange(-radius, radius + 1) ** 2
    dist2 = r2[:, None, None] + r2[:, None] + r2
    body[dist2 <= radius ** 2] = 1
    body[0, :, :] = 0
    body[length - 1, :, :] = 0
    body[:, 0, :] = 0
    body[:, length - 1, :] = 0
    body[:, :, 0] = 0
    body[:, :, length - 1] = 0
    # body[radius,radius,radius] = 2
    body[radius, radius, 1] = np.random.randint(c.low, c.high)
    return body

def cube():
    center = c.GRID_SIZE//2
    volt = np.ones((c.GRID_SIZE, c.GRID_SIZE, c.GRID_SIZE), dtype=int)
    # volt[center, center, center] = 2  # pacemaker in center
    init_volt = np.random.randint(c.low, c.high)
    volt[0,0,0] = init_volt  # pacemaker in upper left corner - starting on surface
    print("Initial pacemaker voltage:", init_volt)
    return volt


