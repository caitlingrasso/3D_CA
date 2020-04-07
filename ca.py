import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import constants

class CA:

    def __init__(self, signal):
        self.voltage = signal  # these are the counters
        self.recharge = np.zeros(signal.shape)

        all_indices = np.indices(signal.shape)
        x = all_indices[0][signal > 1]
        y = all_indices[1][signal > 1]
        z = all_indices[2][signal > 1]
        self.pacemaker = [x[0],y[0],z[0]]

    def get_neighbors(self, a):
        b = np.pad(a, pad_width=1, mode='constant', constant_values=0)
        neigh = np.concatenate((
            b[2:, 1:-1, 1:-1, None], b[:-2, 1:-1, 1:-1, None],
            b[1:-1, 2:, 1:-1, None], b[1:-1, :-2, 1:-1, None],
            b[1:-1, 1:-1, 2:, None], b[1:-1, 1:-1, :-2, None]), axis=3)
        return neigh

    def update(self):
        # Store a copy of the voltage map at the previous time step
        self.v_prev = self.voltage.copy()

        # Getting the neighbors of all cells in the voltage map
        neigh = self.get_neighbors(self.voltage)

        # Update the voltage map
        for x in range(self.voltage.shape[0]):
            for y in range(self.voltage.shape[1]):
                for z in range(self.voltage.shape[2]):
                    if self.voltage[x,y,z]>1:  # Signal within cell decays
                        self.voltage[x,y,z] -= 1
                    if self.recharge[x,y,z] > 0:
                        self.recharge[x,y,z] -= 1
                    if self.recharge[x,y,z] == 0 and np.max(neigh[x,y,z,:]) > self.voltage[x,y,z]:
                        nbors = neigh[x, y, z, :]
                        if len(nbors[nbors > 1])>0:
                            self.voltage[x,y,z] = np.min(nbors[nbors>1]) - 1  # pass the signal and decrement the value of the voltage by one (decay)
        self.voltage[self.v_prev == 0] = 0

        for x in range(self.voltage.shape[0]):
            for y in range(self.voltage.shape[1]):
                for z in range(self.voltage.shape[2]):
                    if self.v_prev[x, y, z] > 1 and self.voltage[x,y,z] == 1:  # If a cell was signaling in the last time step and just "turned off"... start the recharge counter
                        self.recharge[x, y, z] = constants.refractory_time


    def run(self, iterations=constants.CA_ITER, save=False, fn='temp.mp4', axis='off', title=''):
        if save:
            moviewriter = FFMpegWriter()

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_title(title, fontsize=16)
            plt.axis(axis)

            moviewriter.setup(fig, fn, dpi=100)

            for i in range(iterations):
                temp = self.voltage > 0
                temp2 = np.ones(temp.shape)
                all_indices = np.indices((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))
                temp2[all_indices[0][temp], all_indices[1][temp], all_indices[2][temp]] = self.voltage[all_indices[0][temp], all_indices[1][temp], all_indices[2][temp]]

                # Pulses
                if i % constants.pulse_time == 0:
                    self.voltage[self.pacemaker[0], self.pacemaker[1], self.pacemaker[2]] = np.random.randint(constants.low, constants.high)

                cmap = plt.get_cmap('gray')
                voltage_min = 1 #self.voltage_min -- should always be 1
                # voltage_max = 100 if  self.voltage.max()<50 else self.voltage.max()
                voltage_max = constants.high
                norm = plt.Normalize(voltage_min, voltage_max)
                ax.voxels(temp, facecolors=cmap(norm(temp2)), edgecolor=None)
                moviewriter.grab_frame()
                self.update()
                plt.cla()
                plt.axis(axis)
            moviewriter.grab_frame()
            moviewriter.finish()
            plt.close(fig)
        else:
            for _ in range(iterations):
                self.update()
