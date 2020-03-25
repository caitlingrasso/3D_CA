'''
Class for both CAs (grid of cells and voltage map)
updates cells, updates voltages, run simulation
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import constants
from network import Network

class CA:

    def __init__(self, initial_cells, initial_voltage):
        self.cells = initial_cells
        self.voltage = initial_voltage

    def get_neighbors(self, a):
        b = np.pad(a, pad_width=1, mode='constant', constant_values=0)
        neigh = np.concatenate((
            b[2:, 1:-1, 1:-1, None], b[:-2, 1:-1, 1:-1, None],
            b[1:-1, 2:, 1:-1, None], b[1:-1, :-2, 1:-1, None],
            b[1:-1, 1:-1, 2:, None], b[1:-1, 1:-1, :-2, None]), axis=3)
        return neigh

    def update_voltage(self):
        # a and b are diffusion coefficients
        self.voltage = self.voltage * constants.a + (constants.b) * np.sum(self.get_neighbors(self.voltage), axis=3)
        self.voltage[self.cells == 0] = 0
        self.voltage = self.voltage.astype(int)

    def run(self, iterations=constants.CA_ITER, save=False, fn='temp.mp4', axis='off', title='', transparent=True):
        if save:
            moviewriter = FFMpegWriter()

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_title(title, fontsize=16)
            plt.axis(axis)
            if transparent:
                cell_face_color = [1, 1, 1, 0.01]
            else:
                cell_face_color = [1, 1, 1]
            cell_edge_color = None #[0, 0, 0, 0.25]

            moviewriter.setup(fig, fn, dpi=100)

            for _ in range(iterations):
                ax.voxels(self.cells, facecolors=cell_face_color, edgecolor=cell_edge_color)
                voltage_face_colors = np.empty((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE, 4))
                for x in range(self.voltage.shape[0]):
                    for y in range(self.voltage.shape[1]):
                        for z in range(self.voltage.shape[2]):
                            alpha = self.voltage[x, y, z] / 255
                            if alpha > 1:
                                alpha = 1
                            voltage_face_colors[x, y, z] = [0, 0, 0, alpha]
                ax.voxels(self.voltage, facecolors=voltage_face_colors)
                moviewriter.grab_frame()
                self.update_voltage()
                plt.cla()
                plt.axis(axis)
            moviewriter.grab_frame()
            moviewriter.finish()
            plt.close(fig)
        else:
            for _ in range(iterations):
                self.update_voltage()
