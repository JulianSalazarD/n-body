import random

import numpy as np
import pygame

import scipy as sp

from sim2d.body2 import Body2


class Simulation:
    SCALE = 200 / sp.constants.astronomical_unit

    def __init__(self, data):
        self.data = data
        self.WIDTH, self.HEIGHT = 1000, 700
        self.win = None
        self.initialise()

    def initialise(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Planet Simulation")

    def draw(self, planet):
        x = planet.position[0] * Simulation.SCALE + self.WIDTH / 2
        y = planet.position[1] * Simulation.SCALE + self.HEIGHT / 2

        if len(planet.orbit) > 2:
            points = []
            for point in planet.orbit:
                x, y = point
                x = x * Simulation.SCALE + self.WIDTH / 2
                y = y * Simulation.SCALE + self.HEIGHT / 2
                points.append((x, y))

            pygame.draw.lines(self.win, planet.color, False, points, 1)

        pygame.draw.circle(self.win, planet.color, (x, y), planet.radius)

    def mainloop(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(120)
            self.win.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for planet in self.data:
                self.draw(planet)
                planet.euler_method(self.data, 60. * 60. * 24)
            pygame.display.update()

        pygame.quit()


def new_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

""" 
SUN_MASS = 1.9891E30
SUN_RADIUS = 696340
EARTH_MASS = 5.972E24
EARTH_RADIUS = 6371

sun = Body2(5, SUN_MASS, np.array([0., 0., 0.]), np.array([0., 0., 0.]), new_color())
earth = Body2(3, EARTH_MASS, np.array([sp.constants.astronomical_unit, 0., 0.]),
              np.array([0., 2.9E4, 0.]), new_color())
jupyter = Body2(4, 1.898E27, np.array([-5.0 * sp.constants.astronomical_unit, 0., 0.]),
                np.array([0., -1.3E4, 0.]), new_color())

mars = Body2(3.5, 6.39 * 10 ** 23, np.array([-1.524 * sp.constants.astronomical_unit, 0., 0.]),
             np.array([0., 24.077 * 1000, 0.]), new_color())
mercury = Body2(1.5, 3.30 * 10 ** 23, np.array([0.387 * sp.constants.astronomical_unit, 0., 0.]),
                np.array([0., -47.4 * 1000, 0.]), new_color())
venus = Body2(2, 4.8685 * 10 ** 24, np.array([0.723 * sp.constants.astronomical_unit, 0., 0.]),
              np.array([0., -35.02 * 1000, 0.]), new_color())

planets = [sun, earth, mars, mercury, venus]

Simulation(planets).mainloop()
"""
