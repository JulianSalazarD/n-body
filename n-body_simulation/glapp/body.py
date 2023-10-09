import numpy as np
import scipy as sp


class Body:
    def __init__(self, radio, mass, position, velocity):
        self.radio = radio
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def euler_method(self, bodies, dt):
        self.position += self.velocity * dt
        self.velocity += self.update_acceleration(bodies) * dt

    def update_acceleration(self, bodies):
        acceleration = 0.0
        for body in bodies:
            if np.any(bodies.position != self.position):
                acceleration += self.gravitational_acceleration(body)
        return acceleration

    def gravitational_acceleration(self, body):
        diff = body.position - self.position
        return sp.constants.G * body.mass * (diff / (np.linalg.norm(diff) ** 3))
            


