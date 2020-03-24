import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import constants
from ca import CA
from network import Network

def display_grid(grid: np.ndarray, title: str = '', show=True):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title(title, fontsize=16)
    ax.voxels(grid, facecolors='k', edgecolor='k')
    if show:
        plt.show()

def plot_cells_and_signal(cells, voltage, title='', axis='off', transparent=True):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title(title, fontsize=16)
    plt.axis(axis)
    if transparent:
        cell_face_color = [1, 1, 1, 0.01]
    else:
        cell_face_color = [1, 1, 1]
    cell_edge_color = [0, 0, 0, 0.01]

    # voltage_face_colors = np.empty((constants.GRID_SIZE,constants.GRID_SIZE,constants.GRID_SIZE), dtype='object')
    # voltage_face_colors[voltage!=0] = [0, 0, 0, voltage[voltage!=0]/255]

    # for x in range(voltage.shape[0]):
    #     for y in range(voltage.shape[1]):
    #         for z in range(voltage.shape[2]):
    #             voltage_face_colors[x,y,z] = [0, 0, 0, voltage/255]

    ax.voxels(cells, facecolors=cell_face_color, edgecolor=cell_edge_color)
    ax.voxels(voltage, facecolors='k', edgecolor='k')
    plt.show()
