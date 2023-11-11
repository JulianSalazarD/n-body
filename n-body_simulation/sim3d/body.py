import numpy as np
import scipy as sp


# Representar un curpo
class Body:
    def __init__(self, radius, mass, position, velocity):
        self.radius = radius
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.r = 0

    # Actualizar posición
    def euler_method(self, bodies, dt):
        self.position += self.velocity * dt
        acc = self.update_acceleration(bodies)
        self.velocity += acc * dt

    def update_acceleration(self, bodies):
        acceleration = 0.0
        for body in bodies:
            if np.any(body.position != self.position):
                acceleration += self.gravitational_acceleration(body)
        return acceleration

    def gravitational_acceleration(self, body):
        diff = body.position - self.position
        return sp.constants.G * body.mass * (diff / (np.linalg.norm(diff) ** 3))
