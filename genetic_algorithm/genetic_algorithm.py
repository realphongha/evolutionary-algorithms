from abc import ABC, abstractmethod
from typing import List


class Individual(ABC):
    def __init__(self, chromosome=None):
        # chromosome encodes a solution for the problem
        self.chromosome = chromosome
        # fitness means how good this solution is
        if chromosome:
            self.fitness = self.calc_fitness()
        else:
            self.fitness = None

    @abstractmethod
    def display(self):
        # prints the chromosome to screen
        pass

    @abstractmethod
    def random_init(self):
        # randomly initializes an individual
        pass

    @abstractmethod
    def calc_fitness(self):
        # calculates this individual fitness
        pass

    @abstractmethod
    def cross(self, other):
        # crosses with another individual
        pass

    def is_valid(self):
        # is this a valid solution? 
        # override it if needed
        return True

    @abstractmethod
    def __lt__(self, other):
        # for comparing individuals
        pass

    def __eq__(self, other):
        # override it if needed
        return self.chromosome == other.chromosome

    @abstractmethod
    def __hash__(self):
        pass


class GeneticAlgorithm(ABC):
    def __init__(self, population_size: int, elitism: bool = True, 
            debug: bool = True):
        # how many individuals in the population?
        self.population_size = population_size
        # all individuals in current generation
        self.population: List[Individual] = list()
        # keeps best individuals from last generation or not?
        self.elitism = elitism
        # verbose or not?
        self.debug = debug

    @abstractmethod
    def init_population(self):
        # initializes population
        pass

    @abstractmethod
    def init_individual(self):
        # initializes an individual
        pass

    @abstractmethod
    def selection(self):
        # selects some individuals to reproduce next generation
        pass
    
    @abstractmethod
    def crossover(self, population: List[Individual]):
        # does crossover to produce offsprings
        pass

    @abstractmethod
    def mutation(self, population: List[Individual]):
        # mutates the population
        pass

    @abstractmethod
    def can_terminate(self, evolved: bool, gen: int):
        # can the algorithm stop now?
        pass

    def run(self) -> Individual:
        # main loop of the algorithm
        self.init_population()
        # greatest individual of all time
        goat = max(self.population)
        evolved = False 
        gen = 0
        while not self.can_terminate(evolved, gen):
            gen += 1
            if self.debug:
                print("Generation %i:" % gen)
            new_population = self.selection()
            greatest = max(new_population)
            if greatest > goat:
                goat = greatest
                evolved = True
            if self.debug:
                print("Best individual in this generation:")
                greatest.display()
                if evolved:
                    print("Evolved!")
            children = self.crossover(new_population)
            self.mutation(children)
            if self.elitism:
                new_population.extend(children)
            else:
                new_population = children
            self.population = new_population
        print("Stop evolved!")
        print("Greatest of all time:")
        goat.display()
        return goat
