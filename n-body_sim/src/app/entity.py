import numpy as np
import pyrr


class Entity:
    """
        A basic object in the world, with a position and rotation.
    """
    __slots__ = ("position", "eulers", "scale")

    def __init__(self, position: list[float], eulers: list[float]):
        """
            Initialize the entity.

            Parameters:

                position: the position of the entity.

                eulers: the rotation of the entity
                        about each axis.
        """

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

    def update(self, dt: float) -> None:
        """
            Update the object, this is meant to be implemented by
            objects extending this class.

            Parameters:

                dt: framerate correction factor.
        """

        pass

    def get_model_transform(self) -> np.ndarray:
        """
            Returns the entity's model to world
            transformation matrix.
        """

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis=np.array([0, 0, 1], dtype=np.float32),
                theta=np.radians(self.eulers[2]),
                dtype=np.float32
            )
        )

        return pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.position), dtype=np.float32
            )
        )