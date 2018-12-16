__author__ = 'tales.cpadua'

import random

class FruitRand:
    def __init__(self, screen_width, screen_height, block_size):
        self.block_size = block_size
        self.pos_x = random.randrange(0, screen_width, self.block_size)
        self.pos_y = random.randrange(0, screen_height, self.block_size)

    def respawn(self, screen_width, screen_height, snake):
        nice_location = False
        while not nice_location:
            self.pos_x = random.randrange(0, screen_width, self.block_size)
            self.pos_y = random.randrange(0, screen_height, self.block_size)
            for s in snake.segments:
                if self.pos_y == s.pos_y and self.pos_x == s.pos_x:
                    nice_location = False
                    break
                else:
                    nice_location = True

class Fruit(FruitRand):
    def __init__(self, screen_width, screen_height, block_size, randlist):
        FruitRand.__init__(self,screen_width, screen_height, block_size)
        self.randlist = randlist
