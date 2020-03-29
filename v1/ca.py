import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import constants
from network import Network

class CA:

    def __init__(self, body, voltage):
        self.body = body
        self.voltage = voltage
        self.pacemaker = np.argwhere(voltage)
        self.pacemaker = self.pacemaker[0]

    def get_neighbors(self, a):
        b = np.pad(a, pad_width=1, mode='constant', constant_values=0)
        neigh = np.concatenate((
            b[2:, 1:-1, 1:-1, None], b[:-2, 1:-1, 1:-1, None],
            b[1:-1, 2:, 1:-1, None], b[1:-1, :-2, 1:-1, None],
            b[1:-1, 1:-1, 2:, None], b[1:-1, 1:-1, :-2, None]), axis=3)
        return neigh

    def update_voltage(self):
        # a and b are diffusion coefficients
        self.voltage = self.voltage * constants.a + constants.b * np.sum(self.get_neighbors(self.voltage), axis=3)
        # self.voltage = self.normalize(self.voltage)  # squishing voltage from between 0 and 1
        # self.voltage[self.cells == 0] = 0

    def normalize(self, x, x_min=0, x_max=1):
        return (x_max - x_min)/(np.max(x)-np.min(x))*(x-np.max(x))+x_max

    def run(self, iterations=constants.CA_ITER, save=False, fn='temp.mp4', axis='off', title='', transparent=True):
        if save:
            moviewriter = FFMpegWriter()

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_title(title, fontsize=16)
            plt.axis(axis)

            moviewriter.setup(fig, fn, dpi=100)

            for i in range(iterations):

                # Pulses
                if i % constants.pulse_time == 0:
                    self.voltage[self.pacemaker[0], self.pacemaker[1], self.pacemaker[2]] = 255

                cmap = plt.get_cmap('binary')
                norm = plt.Normalize(self.voltage.min(), self.voltage.max())
                ax.voxels(np.ones_like(self.voltage), facecolors=cmap(norm(self.voltage)), edgecolor=None)
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

    def run2(self, iterations=constants.CA_ITER, save=False, fn='temp.mp4', axis='off', title=''):
        if save:
            moviewriter = FFMpegWriter()

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_title(title, fontsize=16)
            plt.axis(axis)

            moviewriter.setup(fig, fn, dpi=100)

            for i in range(iterations):

                # Pulses
                if i % constants.pulse_time == 0:
                    self.voltage[self.pacemaker[0], self.pacemaker[1], self.pacemaker[2]] = self.voltage[self.pacemaker[0], self.pacemaker[1], self.pacemaker[2]] + 255

                voltage_face_colors = np.empty((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE, 4))
                body_face_colors = np.empty((constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE, 4))
                norm_bod = plt.Normalize(self.body.min(), self.body.max())
                norm_volt = plt.Normalize(self.voltage.min(), self.voltage.max())
                alpha_bod = norm_bod(self.body)
                alpha_volt = norm_volt(self.voltage)
                for x in range(self.body.shape[0]):
                    for y in range(self.body.shape[1]):
                        for z in range(self.body.shape[2]):
                            body_face_colors[x, y, z] = [1, 1, 1, alpha_bod[x, y, z]]
                            voltage_face_colors[x, y, z] = [0, 0, 0, alpha_volt[x, y, z]]
                ax.voxels(self.body, facecolors=body_face_colors)
                ax.voxels(self.voltage, facecolors=voltage_face_colors)


                moviewriter.grab_frame()
                self.voltage = self.voltage * constants.a + constants.b * np.sum(self.get_neighbors(self.voltage),
                                                                                 axis=3)
                self.voltage[self.body == 0] = 0
                plt.cla()
                plt.axis(axis)
            moviewriter.grab_frame()
            moviewriter.finish()
            plt.close(fig)
        else:
            for _ in range(iterations):
                self.voltage = self.voltage * constants.a + constants.b * np.sum(self.get_neighbors(self.voltage),
                                                                                 axis=3)
                self.voltage[self.cells == 0] = 0
