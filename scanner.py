#from PIL import Image
from datetime import datetime

from selenium.webdriver.common.by import By

# https://github.com/boppreh/keyboard
import keyboard
import mss
import pyscreenshot as ImageGrab

import numpy as np

def obstacle(distance, length, speed, time):
    return { 'distance': distance, 'length': length, 'speed': speed, 'time': time }

class Scanner:
    def __init__(self):
        self.dino_start = (0, 0)
        self.dino_end = (0, 0)
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False
        self.sct = mss.mss()
        self.counter = 0

    def locate_game(self, browser, game_width = 600, game_height = 40):
        
        element = browser.find_element(By.ID, "main-frame-error")
        game_location = element.location
        print(game_location)

        game_location['w'] = game_width
        game_location['h'] = game_height

        self.game_location = {
            'left': game_location['x'],
            'top': game_location['y'],
            'width': game_location['w'],
            'height': game_location['h']
        }

        # self.dino_start = (game_location['x'], game_location['y'])
        # self.dino_end = (game_location['w'], game_location['h'])

    def set_view(self, view = 'front'):
        
        if view == 'front':
            box = self.game_location.copy()

            # Front View Setting
            box['left'] += 42
            box['top'] += 42 * 2
            # box['h'] -= 30

            return box

    def __next_obstacle_dist(self, bbox):

        image = self.sct.grab(bbox)
        numpy_image = np.asarray(image)

        with open(f'./numpy/ss_{self.counter}.npy', 'wb') as file:
            np.save(file, numpy_image)
            self.counter += 1
        location = np.where(np.min(numpy_image[:,:,0], axis = 0) == 83)[0]

        if any(location):
            return location[0]
        else:
            return 600

    def find_next_obstacle(self):
        
        bbox = self.set_view()
        current_obstacle = self.__next_obstacle_dist(bbox)

        if current_obstacle < 45 and not self.__change_fitness:
            self.__current_fitness += 1
            self.__change_fitness = True
        elif current_obstacle > 45:
            self.__change_fitness = True
        
        time_ = datetime.now()
        delta_dist = 0
        speed = 0
        
        if self.last_obstacle:
            delta_dist = self.last_obstacle['distance'] - current_obstacle
            speed = (delta_dist / ((time_ - self.last_obstacle['time']).microseconds)) * 10000
        
        self.last_obstacle = obstacle(current_obstacle, 1, speed, time_)
        return self.last_obstacle

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
