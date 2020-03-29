import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import constants
from ca import CA
from network import Network

def plot_voxels(a):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.axis('off')
    cmap = plt.get_cmap("binary")
    norm = plt.Normalize(a.min(), a.max())
    ax.voxels(np.ones_like(a), facecolors=cmap(norm(a)), edgecolor=None)
    plt.show()

def plot_body_and_voltage(body, voltage, title='', axis='off', transparent=True):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title(title, fontsize=16)
    plt.axis(axis)

    body_face_colors = np.empty((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE, 4))
    norm = plt.Normalize(body.min(), body.max())
    alpha = norm(body)
    for x in range(body.shape[0]):
        for y in range(body.shape[1]):
            for z in range(body.shape[2]):
                body_face_colors[x, y, z] = [1, 1, 1, alpha[x, y, z]]
    ax.voxels(body, facecolors=body_face_colors)

    voltage_face_colors = np.empty((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE, 4))
    norm = plt.Normalize(voltage.min(), voltage.max())
    alpha = norm(voltage)
    for x in range(body.shape[0]):
        for y in range(body.shape[1]):
            for z in range(body.shape[2]):
                voltage_face_colors[x, y, z] = [0, 0, 0, alpha[x,y,z]]
    ax.voxels(voltage, facecolors=voltage_face_colors)
    plt.show()