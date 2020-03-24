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

    def update_cells(self, network: Network):
        # Pad arrays so the indices when growing are not out of bounds
        self.cells = np.pad(self.cells, pad_width=1, mode='constant', constant_values=0)
        self.voltage = np.pad(self.voltage, pad_width=1, mode='constant', constant_values=0)

        # Inputs: presence/absence of 4 neighbors and voltages of 4 neighbors
        inputs = np.concatenate((self.get_neighbors(self.cells), self.get_neighbors(self.voltage)), axis=2)

        # Initialize empty outputs array
        # Outputs: down, up, right, left, grow/no_grow, voltage
        outputs = np.zeros((inputs.shape[0], inputs.shape[1], constants.OUTPUTS), dtype=int)

        # Feed inputs into the neural network for each cell that is on
        outputs[self.cells==1] = network.forward_prop(inputs[self.cells==1])

        # Update voltage of all cells that are on
        self.voltage[self.cells==1] = outputs[self.cells==1][:, constants.OUTPUTS - 1]

        # Include global 'off' switch? (Grow/no grow bit)
        all_indices = np.indices((constants.GRID_SIZE + 2, constants.GRID_SIZE + 2))  # plus 2 because of the padding
        if constants.no_grow_flag == False:
            outputs[:, :, 4] = 1

        # Grow down
        grow_down = (outputs[:, :, 4] == 1) & (
                outputs[:, :, 0] == 1)  # the location of cells in the 9x9 grid that should replicate down
        self.cells[all_indices[0][grow_down]+1, all_indices[1][grow_down]] = 1
        self.voltage[all_indices[0][grow_down]+1, all_indices[1][grow_down]] = outputs[grow_down][:,constants.OUTPUTS-1]

        # Grow up
        grow_up = (outputs[:, :, 4] == 1) & (
                    outputs[:, :, 1] == 1)
        self.cells[all_indices[0][grow_up] - 1, all_indices[1][grow_up]] = 1
        self.voltage[all_indices[0][grow_up] - 1, all_indices[1][grow_up]] = outputs[grow_up][:, constants.OUTPUTS - 1]

        # Grow right
        grow_right = (outputs[:, :, 4] == 1) & (
                outputs[:, :, 2] == 1)
        self.cells[all_indices[0][grow_right], all_indices[1][grow_right]+1] = 1
        self.voltage[all_indices[0][grow_right], all_indices[1][grow_right]+1] = outputs[grow_right][:, constants.OUTPUTS - 1]

        # Grow left
        grow_left = (outputs[:, :, 4] == 1) & (
                outputs[:, :, 3] == 1)
        self.cells[all_indices[0][grow_left], all_indices[1][grow_left] - 1] = 1
        self.voltage[all_indices[0][grow_left], all_indices[1][grow_left] - 1] = outputs[grow_left][:,
                                                                                   constants.OUTPUTS - 1]
        # Remove padding
        self.cells = self.cells[1:-1, 1:-1]
        self.voltage = self.voltage[1:-1, 1:-1]

    def get_neighbors_2d(self, a):
        b = np.pad(a, pad_width=1, mode='constant', constant_values=0)
        print(b[2:, 1:-1, None].shape)
        neigh = np.concatenate((b[2:, 1:-1, None], b[:-2, 1:-1, None],
            b[1:-1, 2:, None], b[1:-1, :-2, None]), axis=2)
        return neigh

    def get_neighbors(self, a):
        b = np.pad(a, pad_width=1, mode='constant', constant_values=0)
        neigh = np.concatenate((
            b[2:, 1:-1, 1:-1, None], b[:-2, 1:-1, 1:-1, None],
            b[1:-1, 2:, 1:-1, None], b[1:-1, :-2, 1:-1, None],
            b[1:-1, 1:-1, 2:, None], b[1:-1, 1:-1, :-2, None]), axis=3)
        return neigh

    def update_voltage(self):
        # Chemical diffusion equation from Miller
        self.voltage = self.voltage * 0.5 + (1 / 16) * np.sum(self.get_neighbors(self.voltage), axis=3)
        self.voltage = self.voltage.astype(int)

    def run(self, iterations, network:Network):
        for _ in range(iterations):
            self.update_voltage()
            # self.update_cells(network)

    def run_and_save(self, fn, iterations=constants.CA_ITER, axis='on', title=''):

        moviewriter = FFMpegWriter()

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_title(title, fontsize=16)
        plt.axis(axis)
        cell_face_color = [1, 1, 1, 0.01]
        cell_edge_color = [0, 0, 0, 0.25]
        ax.voxels(self.cells, facecolors=cell_face_color, edgecolor=cell_edge_color)
        ax.voxels(self.voltage, facecolors='k', edgecolor='k')

        moviewriter.setup(fig, fn, dpi=100)

        for _ in range(iterations):
            # ax.voxels(self.cells, facecolors=cell_face_color, edgecolor=cell_edge_color)
            ax.voxels(self.voltage, facecolors='k', edgecolor='k')
            moviewriter.grab_frame()
            self.update_voltage()

        moviewriter.grab_frame()
        moviewriter.finish()
        plt.close(fig)

