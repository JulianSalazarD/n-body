from sim3d.body import Body


# Representar un curpo para simulacon 2d
class Body2(Body):
    def __init__(self, radius, mass, position, velocity, color):
        super().__init__(radius, mass, position, velocity)
        self.r = 0
        self.orbit = []
        self.color = color

    def euler_method(self, bodies, dt):
        self.position += self.velocity * dt
        acc = self.update_acceleration(bodies)
        self.velocity += acc * dt

        self.orbit.append((self.position[0], self.position[1]))

        if (abs(self.orbit[0][0] - self.orbit[-1][0]) < 100000 and abs(self.orbit[0][1] - self.orbit[-1][1]) < 100000
                and len(self.orbit) > 2):
            self.orbit.clear()
