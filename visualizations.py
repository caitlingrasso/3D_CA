import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import constants
from ca import CA
from network import Network

def display_grid(grid: np.ndarray, title: str = '', show=True, colormap = constants.COLOR_MAP_CELLS):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title(title, fontsize=16)
    ax.voxels(grid, facecolors='k', edgecolor='k')
    if show:
        plt.show()

def plot_cells_and_signal(cells, voltage, title='', axis='on'):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title(title, fontsize=16)
    plt.axis(axis)
    cell_face_color = [1, 1, 1, 0.01]
    cell_edge_color = [0, 0, 0, 0.25]

    # voltage_face_colors = np.empty((constants.GRID_SIZE,constants.GRID_SIZE,constants.GRID_SIZE), dtype='object')
    # voltage_face_colors[voltage!=0] = [0, 0, 0, voltage[voltage!=0]/255]

    # for x in range(voltage.shape[0]):
    #     for y in range(voltage.shape[1]):
    #         for z in range(voltage.shape[2]):
    #             voltage_face_colors[x,y,z] = [0, 0, 0, voltage/255]

    ax.voxels(cells, facecolors=cell_face_color, edgecolor=cell_edge_color)
    ax.voxels(voltage, facecolors='k', edgecolor='k')
    plt.show()

def save_movies(ic_cells, ic_voltage, fn_cells, fn_voltage, weights=[], iterations = constants.CA_ITER):
    ca = CA(ic_cells, ic_voltage)
    if len(weights) != 0:
        nn = Network(weights)
    else:
        nn = Network()
    ca.run_and_save(iterations, nn, cells_mov_FN=fn_cells, voltage_mov_FN=fn_voltage)

def save_final_state(ic_cells, ic_voltage, fn, title='', weights=[], iterations = constants.CA_ITER):
    ca = CA(ic_cells, ic_voltage)
    if len(weights) != 0:
        nn = Network(weights)
    else:
        nn = Network()
    ca.run(iterations, nn)
    fig, ax = plt.subplots()
    fig.suptitle(title, fontsize=16)
    ax.matshow(ca.cells, cmap=constants.COLOR_MAP_CELLS)
    plt.savefig(fn)
    plt.close(fig)

def playback(wts, init_cells, init_voltage, ca_iter=constants.CA_ITER, title=''):
    if type(wts)!=list:
        wts = [wts]
    if type(init_cells) != list:
        init_cells =[init_cells]
    if type(init_voltage) != list:
        init_voltage =[init_voltage]
    for i, wt in enumerate(wts):
        nn = Network(wt)
        for ic in init_cells:
            for iv in init_voltage:
                ca = CA(ic, iv)
                fig, ax = plt.subplots()
                # title = 'i: {}'.format(i)
                fig.suptitle(title, fontsize=16)
                mat = ax.matshow(ic, cmap=constants.COLOR_MAP_CELLS)
                _ = animation.FuncAnimation(fig,
                                            ani_update,
                                            repeat=False,
                                            fargs=(ca, nn, plt, ca_iter, mat,),
                                            interval=ca_iter)
                plt.show()


def ani_update(frame: int, *fargs: tuple):
    ca, nn, plt, ca_iter, mat = fargs  # unpack tuple
    if frame<=ca_iter:
        ca.update_voltage()
        ca.update_cells(nn)
        mat.set_data(ca.cells)
        # print(frame)
        return ca.cells
    else:
        plt.close()
