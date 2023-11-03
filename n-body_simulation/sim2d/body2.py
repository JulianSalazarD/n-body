import numpy as np
import scipy as sp


class Body2:
    def __init__(self, radius, mass, position, velocity, color):
        self.radius = radius
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.r = 0
        self.bigger = False
        self.orbit = []
        self.color = color

    def euler_method(self, bodies, dt):
        self.position += self.velocity * dt
        acc = self.update_acceleration(bodies)
        self.velocity += acc * dt

        self.orbit.append((self.position[0], self.position[1]))

        if (abs(self.orbit[0][0] - self.orbit[-1][0]) < 1 and abs(self.orbit[0][1] - self.orbit[-1][1]) < 1
                and len(self.orbit) > 2):
            self.orbit.clear()
            print(len(self.orbit))

    def update_acceleration(self, bodies):
        acceleration = 0.0
        for body in bodies:
            if np.any(body.position != self.position):
                acceleration += self.gravitational_acceleration(body)
        return acceleration

    def gravitational_acceleration(self, body):
        diff = body.position - self.position
        return sp.constants.G * body.mass * (diff / (np.linalg.norm(diff) ** 3))

    def circular(self):
        pass
