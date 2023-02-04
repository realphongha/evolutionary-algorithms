import numpy as np
from typing import Tuple
from .ga_nn import FCNeuralNetwork


class SnakeFCNN(FCNeuralNetwork):
    def __call__(self, x):
        pass

    def __init__(self, board_shape: Tuple(int, int)):
        super().__init__()
        self.board_size = board_shape[0] * board_shape[1] 
        self.layers = (self.board_size, self.board_size, 5) 
        self.weights = list()
        for i, num_neural in enumerate(self.layers):
            if i == len(self.layers) - 1: break
            num_neural_next = self.layers[i+1]
            self.weights.append(
                np.zeros((num_neural, num_neural_next))
            )

    def _init_weights_random(self):
        self.weights = list()
        for i, num_neural in enumerate(self.layers):
            if i == len(self.layers) - 1: break
            num_neural_next = self.layers[i+1]
            self.weights.append(
                np.random.rand(num_neural, num_neural_next) * 2 - 1 
            )


class SnakeGANN:
    def __init__(self):
        self.fcnn = FCNeuralNetwork