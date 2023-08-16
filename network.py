import numpy as np
import os
class Network:
    def __init__(self):
        self.input_size = 3
        self.hidden_size_1 = 5
        self.hidden_size_2 = 4
        self.output_size = 1
        self.W1 = np.random.randn(self.input_size, self.hidden_size_1)
        self.W2 = np.random.randn(self.hidden_size_1, self.hidden_size_2)
        self.W3 = np.random.randn(self.hidden_size_2, self.output_size)
        self.fitness = 0

    def forward(self, inputs):
        self.z2 = np.dot(inputs, self.W1)
        self.a2 = np.tanh(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        self.a3 = np.tanh(self.z3)
        self.z4 = np.dot(self.a3, self.W3)
        yHat = np.tanh(self.z4)
        return yHat

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def save(self, generation_id, genome_id):
        os.mkdir(f'./model/{generation_id}/weight_{genome_id}/')
        for weight_id, weight in enumerate([self.W1, self.W2, self.W3], 1):
            with open(f'./model/{generation_id}/weight_{genome_id}/W{weight_id}.npy', 'wb') as file:
                np.save(file, weight)

    def load(self, generation_id, genome_id):
        
        with open(f'./model/{generation_id}/weight_{genome_id}/W1.npy', 'rb') as file:
            self.W1 = np.load(file)

        with open(f'./model/{generation_id}/weight_{genome_id}/W2.npy', 'rb') as file:
            self.W2 = np.load(file)

        with open(f'./model/{generation_id}/weight_{genome_id}/W3.npy', 'rb') as file:
            self.W3 = np.load(file)