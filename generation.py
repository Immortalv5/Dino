from scanner import Scanner
from network import Network

from time import sleep
import numpy as np

# https://github.com/boppreh/keyboard
import keyboard

import random
import copy

class Generation:
    def __init__(self):
        self.__genomes = [Network() for i in range(1)]
        self.__best_genomes = []

    def execute(self):

        scanner = Scanner()
        scanner.locate_game()
        
        r = range(1,2)
        
        for num, genome in zip(r, self.__genomes):
            
            print('genome_' + str(num))
            
            scanner.reset()
            keyboard.press_and_release('ctrl', 'r')
            sleep(1)
            keyboard.press_and_release('space')
            
            while True:
                try:
                    obs = scanner.find_next_obstacle()
                    inputs = [obs['distance'] / 1000, obs['length'], obs['speed']/10]
                    print(inputs)
                    outputs = genome.forward(np.array(inputs, dtype=float))
                    print(outputs)
                    if outputs[0] > 0.5:
                        keyboard.press_and_release('space')
                    print('continue')
                except:
                    break
            print("Improved")
            genome.fitness = scanner.get_fitness()

    def keep_best_genomes(self):
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.__best_genomes = self.__genomes[:]
        print(self.__best_genomes)

    def mutations(self):
        while len(self.__genomes) < 10:
            genome1 = random.choice(self.__best_genomes)
            genome2 = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(self.cross_over(genome1, genome2)))
        while len(self.__genomes) < 12:
            genome = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(genome))

    def cross_over(self, genome1, genome2):
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)
        cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]
        cut_location = int(len(new_genome.W2) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]
        return new_genome

    def __mutate_weights(self, weights):
        if random.uniform(0, 1) < 0.2:
            return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)
        new_genome.W1 += self.__mutate_weights(new_genome.W1)
        new_genome.W2 += self.__mutate_weights(new_genome.W2)
        return new_genome
