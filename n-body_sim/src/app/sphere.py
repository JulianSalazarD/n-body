from src.app.entity import Entity


class Sphere(Entity):
    """
        A basic object in the world, with a position and rotation.
    """
    __slots__ = tuple([])

    def __init__(self, position: list[float], eulers: list[float], scale: list[float]):
        """
            Initialize the cube.

            Parameters:

                position: the position of the entity.

                eulers: the rotation of the entity
                        about each axis.
        """

        super().__init__(position, eulers, scale)

    def update(self, dt: float, pos=None) -> None:
        """
            Update the cube.

            Parameters:

                dt: framerate correction factor.
        """

        self.eulers[2] += 0.25 * dt

        if self.eulers[2] > 360:
            self.eulers[2] -= 360

        if pos is not None:
            self.update_object_position(pos[0], pos[1], pos[2])

    def update_object_position(self, x, y, z):
        self.position = [x, y, z]
