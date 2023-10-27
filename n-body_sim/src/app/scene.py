import numpy as np

from src.app.PointLight import PointLight
from src.app.camera import Camera
from src.app.entity import Entity
from src.app.sphere import Sphere

ENTITY_TYPE = {
    "SPHERE": 0,
    "POINTLIGHT": 1,
}


class Scene:
    """
        Manages all objects and coordinates their interactions.
    """
    __slots__ = ("entities", "camera")

    def __init__(self):
        """
            Initialize the scene.
        """

        self.entities: dict[int, list[Entity]] = {
            ENTITY_TYPE["SPHERE"]: [
                Sphere(position=[0, 0, 0], eulers=[0, 0, 0]),
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

        for entities in self.entities.values():
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
