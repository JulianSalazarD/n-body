import numpy as np

from src.app.PointLight import PointLight
from src.app.camera import Camera
from src.app.entity import Entity
from src.app.sphere import Sphere

ENTITY_TYPE = {
    "SPHERE": 0,
    "POINTLIGHT": 1,
}

c = 1875e5


class Scene:
    """
        Manages all objects and coordinates their interactions.
    """
    __slots__ = ("entities", "camera", "x", "y")

    def __init__(self, bodies):
        """
            Initialize the scene.
        """
        self.x = bodies
        # print([bodies[1].position[0] / c, bodies[1].position[1] / c, bodies[1].position[2] / c])
        self.y = [[bodies[1].position[0] / c, bodies[1].position[1] / c, bodies[1].position[2] / c]]
        self.entities: dict[int, list[Entity]] = {
            ENTITY_TYPE["SPHERE"]: [
                Sphere(position=self.y[0],
                       eulers=[0, 0, 0], scale=[50, 50, 50]),
            ],

            ENTITY_TYPE["POINTLIGHT"]: [
                PointLight(
                    position=[
                        np.random.uniform(low=3.0, high=9.0),
                        np.random.uniform(low=-2.0, high=2.0),
                        np.random.uniform(low=0.0, high=4.0)],
                    color=[
                        np.random.uniform(low=0.5, high=1.0),
                        np.random.uniform(low=0.5, high=1.0),
                        np.random.uniform(low=0.5, high=1.0)],
                    strength=3)
                for _ in range(8)
            ],
        }

        self.camera = Camera(
            position=[-200, 0, 0]
        )

    def update(self, dt: float) -> None:
        """
            Update all objects in the scene.

            Parameters:

                dt: framerate correction factor
        """

        # for entities in self.entities.values():
        #    for entity in entities:
        #        entity.update(dt)
        entities = self.entities[0]
        print(self.y[0])
        # self.y[0] = [self.y[0][0]-0.1, 0, 0]
        for entity in entities:
            entity.update(dt, self.y[0])
        self.update_position()
        self.update_window()
        entities = self.entities[1]
        for entity in entities:
            entity.update(dt)

        self.camera.update(dt)

    def move_camera(self, d_pos: list[float]) -> None:
        """
            move the player by the given amount in the
            (forwards, right, up) vectors.
        """

        self.camera.move(d_pos)

    def spin_camera(self, d_eulers: list[float]) -> None:
        """
            spin the player by the given amount
            around the (x,y,z) axes
        """

        self.camera.spin(d_eulers)

    def update_position(self):
        for body in self.x:
            body.euler_method(self.x, 60. * 60. * 24)
            # if body.radius == 30: print(body.position)

    def update_window(self):
        # for sphere in range(len(self.sphere)):
        #    self.sphere[sphere].set_move_translate(pygame.Vector3(-self.positions[sphere][0],
        # -self.positions[sphere][1],
        # -self.positions[sphere][2]))
        # self.positions[body] = -self.positions[body]
        # print(self.positions[body])
        self.y[0] = [self.x[0].position[0] / c, self.x[0].position[1] / c, self.x[0].position[2] / c]
