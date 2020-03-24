'''
Class for a vanilla fully-connected network, no hidden layers
'''

import numpy as np
import constants

class Network:

    #input_node_name =[]
    #output_node_names = []
    #activation_functions = []

    def __init__(self, weights):
        self.n_x = constants.INPUTS
        self.n_y = constants.OUTPUTS
        self.weights = np.reshape(weights, (self.n_y, self.n_x))

    def forward_prop(self, inputs):
        '''
        Implement forward propagation to calculate outputs
        :param inputs: matrix of inputs for multiple samples/cells
        :return: matrix of outputs
        '''
        w_binary_nodes = self.weights[0:self.n_y - 1, :]  # all weights except the last column
        Z1 = np.dot(inputs, w_binary_nodes.transpose())
        A1 = self.sigmoid(Z1)
        out1 = self.predict(A1).astype(int)

        w_last_node = self.weights[self.n_y - 1, :]
        Z1_last_node = np.dot(inputs, w_last_node.transpose())
        A1_last_node = self.rescaled_positive_sigmoid(Z1_last_node).astype(int)
        A1_last_node = np.reshape(A1_last_node, (inputs.shape[0], 1))

        outputs = np.concatenate((out1, A1_last_node), axis=1)

        return outputs



    def sigmoid(self, x):
        s = 1 / (1 + np.exp(-x))
        return s

    def rescaled_positive_sigmoid(self, x, x_min=0, x_max=255):
        return (x_max - x_min) * self.sigmoid(x) + x_min

    def predict(self, hyp):
        # prediction = np.matrix(np.zeros(hyp.shape))
        prediction = hyp > 0.5
        return prediction.astype(int)
