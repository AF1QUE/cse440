import neat
import pygame
import math

WIDTH = 1920
HEIGHT = 1080
CAR_SIZE_X = 60
CAR_SIZE_Y = 60
BORDER_COLOR = (255, 255, 255, 255)

class Car:
    def __init__(self):
        self.sprite = pygame.image.load('car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite
        self.position = [830, 920]
        self.angle = 0
        self.speed = 0
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]
        self.alive = True


    def update(self, game_map):
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed