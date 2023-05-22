#from PIL import Image
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

# https://github.com/boppreh/keyboard
import keyboard
import pyscreenshot as ImageGrab

dino_color = (83, 83, 83)

def screenshot(x, y, w, h):
    
    bbox = (x, y, w, h)
    im = ImageGrab.grab(bbox)
    return im
  
def is_dino_color(pixel):
    return pixel == (83, 83, 83)

def obstacle(distance, length, speed, time):
    return { 'distance': distance, 'length': length, 'speed': speed, 'time': time }

class Scanner:
    def __init__(self):
        self.dino_start = (0, 0)
        self.dino_end = (0, 0)
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def locate_game(self, game_width = 600, game_height = 150, ground_size = 40):
        
        browser = webdriver.Firefox()
        browser.fullscreen_window()
        # browser.maximize_window()
        browser.get("https://trex-runner.com")

        element = browser.find_element(By.ID, "main-frame-error")
        game_location = element.location

        game_location['w'] = game_location['x'] + game_width
        game_location['h'] = game_location['y'] + game_height - ground_size

        self.game_location = list(game_location.values())

        # self.dino_start = (game_location['x'], game_location['y'])
        # self.dino_end = (game_location['w'], game_location['h'])

    def set_view(self, view = 'front'):
        
        if view == 'front':
            box = self.game_location.copy()

            # Front View Setting
            box['x'] += 42
            box['y'] += 42 * 2
            box['h'] -= 36

            return list(box.values())

    def find_next_obstacle(self, dino_size = 41):
        
        bbox = self.set_view()
        image = ImageGrab.grab(bbox)

        dist_2 = self.__next_obstacle_dist(image)
        # if dist_2 < 45 and not self.__change_fitness:
        #     self.__current_fitness += 1
        #     self.__change_fitness = True
        # elif dist_2 > 45:
        #     self.__change_fitness = False
        time = datetime.now()
        delta_dist = 0
        speed = 0
        if self.last_obstacle:
            delta_dist = self.last_obstacle['distance'] - dist_2
            speed = (delta_dist / ((time - self.last_obstacle['time']).microseconds)) * 10000
        self.last_obstacle = obstacle(dist_2, 1, speed, time)
        return self.last_obstacle

    def __next_obstacle_dist(self, image):
        s = 0
        size = image.size
        # for y in range(0, size[1], 5):
        #     for x in range(0, size[0], 5):
        #         color = image.getpixel((x, y))
        #         if is_dino_color(color):
        #             s += 1
        # if s > 50:
        #     raise Exception('Game over!')

        for x in range(0, size[0], 5):
            for y in range(0, size[1], 5):
                color = image.getpixel((x, y))
                if is_dino_color(color):
                    return x
        return 1000000

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
