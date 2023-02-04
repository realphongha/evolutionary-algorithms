import pickle
import numpy as np
from abc import ABC, abstractmethod
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm, Individual


class FCNeuralNetwork:
    def __init__(self): 
        self.layers = list()
        self.weights = None 

    @abstractmethod
    def __call__(self, x):
        pass

    def save(self, save_path):
        with open(save_path, "wb") as file:
            pickle.dump((self.layers, self.weights), file)
    
    def load(self, save_path):
        with open(self, save_path, "rb") as file:
            self.layers, self.weights = pickle.load(file)
