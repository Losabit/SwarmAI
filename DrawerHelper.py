import pygame
import sys
from pygame.locals import *


class DrawerHelper:
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, title, width, height):
        # set up pygame
        pygame.init()
        # set up the window
        pygame.display.set_caption(title)
        self.windowSurface = pygame.display.set_mode((width, height), 0, 32)
        self.windowSurface.fill(self.WHITE)

    def draw_background(self, color):
        self.windowSurface.fill(color)

    def draw_line(self, color, pos_1, pos_2, width=1):
        pygame.draw.line(self.windowSurface, color, pos_1, pos_2, width)

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.windowSurface, color, rect)

    def draw_ellipse(self, color, rect, width=1):
        pygame.draw.ellipse(self.windowSurface, color, rect, width)

    def draw_circle(self, color, center, radius,  width=1):
        pygame.draw.ellipse(self.windowSurface, color, center, radius, width)

    def draw_polygon(self, color, points, width=1):
        pygame.draw.polygon(self.windowSurface, color, points, width)

    def draw_arc(self, color, rect, start_angle, end_angle):
        pygame.draw.arc(self.windowSurface, color, rect, start_angle, end_angle)

    def get_window_surface(self):
        return self.windowSurface
