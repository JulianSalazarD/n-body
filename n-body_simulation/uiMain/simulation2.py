import pygame
import scipy as sp

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Simulation:
    view = 200
    SCALE = view / sp.constants.astronomical_unit

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
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and Simulation.view < 460:
                    Simulation.view += 5
                if keys[pygame.K_DOWN] and Simulation.view > 20:
                    Simulation.view -= 5
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and Simulation.view < 460:
                        Simulation.view += 5
                    elif event.button == 5 and Simulation.view > 20:
                        Simulation.view -= 5
                Simulation.SCALE = Simulation.view / sp.constants.astronomical_unit

            for planet in self.data:
                self.draw(planet)
                planet.euler_method(self.data, 60. * 60. * 24)
            pygame.display.update()

        pygame.quit()
