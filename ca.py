import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import constants

class CA:

    def __init__(self, signal):
        self.voltage = signal  # these are the counters
        self.recharge = np.zeros(signal.shape)  # increments every time step its on signal value is greater than 0... signal
        # can only pass to cells with a recharge value of 0... once the recharge value of a cell hits the refactory
        # period (constant) the value goes back to zero
        all_indices = np.indices(signal.shape)
        x = all_indices[0][signal == 2]
        y = all_indices[1][signal == 2]
        z = all_indices[2][signal == 2]
        self.pacemaker = [x[0],y[0],z[0]]
        self.recharge[self.pacemaker] = 1

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

        # Signal dies for all cells that go over the max signal (max_signal determines how far the signal can propagate)
        self.voltage[self.voltage > constants.max_signal] = 1

        # Getting the neighbors of all cells in the voltage map
        neigh = self.get_neighbors(self.voltage)

        # Update the voltage map !!
        for x in range(self.voltage.shape[0]):
            for y in range(self.voltage.shape[1]):
                for z in range(self.voltage.shape[2]):
                    if self.recharge[x,y,z] > constants.refactory_time:
                        self.recharge[x, y, z] = 0
                        self.voltage[x,y,z]=1
                    if self.recharge[x,y,z] == 0 and np.max(neigh[x,y,z,:]) > 1:  # cell takes the max value of its neighbors
                        self.voltage[x,y,z] = np.max(neigh[x,y,z,:]) + 1  # increment time the "trail" has been alive
                    if (self.voltage[x, y, z] > 1):  # increment time cell has been "lit"
                        self.recharge[x, y, z] += 1
        self.voltage[self.v_prev==0]=0
        # print(self.voltage)

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
                    self.voltage[self.pacemaker[0], self.pacemaker[1], self.pacemaker[2]] = 2
                    self.recharge[:,:,:]=0

                cmap = plt.get_cmap('binary')
                norm = plt.Normalize(self.voltage.min(), self.voltage.max())
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

    # def update_vectorized(self):
    #     #TODO: fix!!
    #
    #     # self.voltage = self.voltage-1 + np.max(self.get_neighbors(self.voltage), axis=3)
    #     all_indices = np.indices((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))
    #     neigh = self.get_neighbors(self.voltage)
    #     print(self.voltage)
    #     self.voltage[all_indices[0][self.recharge==0], all_indices[1][self.recharge==0]] = \
    #         np.max(neigh[all_indices[0][self.recharge==0], all_indices[1][self.recharge==0]], axis=2) + 1  # only is the max of the neighbors is not equal to 0
    #     print(self.voltage)
