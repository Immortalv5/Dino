from scanner import Scanner
from network import Network

from time import sleep
import numpy as np

# https://github.com/boppreh/keyboard
import keyboard
from selenium import webdriver

import random
import copy

class Generation:
    def __init__(self):
        self.__genomes = [Network() for i in range(3)]
        self.__best_genomes = []

        self.browser = webdriver.Firefox()
        self.browser.fullscreen_window()
        # browser.maximize_window()
        self.browser.get("https://trex-runner.com")

    def execute(self):

        scanner = Scanner()
        scanner.locate_game(self.browser)
        
        r = range(1,4)
        
        for num, genome in zip(r, self.__genomes):
            
            print('genome_' + str(num))
            
            scanner.reset()
            keyboard.press_and_release('ctrl', 'r')
            sleep(1)
            keyboard.press_and_release('space')
            
            while True:

                obs = scanner.find_next_obstacle()
                print(obs)
                inputs = [obs['distance'] / 600, obs['length'], obs['speed']/10]
                outputs = genome.forward(np.array(inputs, dtype=float))
                print(outputs)
                if outputs[0] > 0.5:
                    keyboard.press_and_release('space')
                sleep(0.1)

            print("Improved")
            genome.fitness = scanner.get_fitness()

    def keep_best_genomes(self):
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.__best_genomes = self.__genomes[:]
        print(self.__best_genomes)
    
    def save_genomes(self, generation_id):
        for genome_id, genome in enumerate(self.__best_genomes, 1):
            genome.save(generation_id, genome_id)

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
