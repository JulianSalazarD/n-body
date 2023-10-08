from .Mesh import *


class Axes(Mesh):
    def __init__(self, program_id, location):
        vertices = [[-250.0, 0.0, 0.0],
                    [250.0, 0.0, 0.0],
                    [0.0, -250.0, 0.0],
                    [0.0, 250.0, 0.0],
                    [0.0, 0.0, -250.0],
                    [0.0, 0.0, 250.0]]

        colors = [[1.0, 0.0, 0.0],
                  [1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [1.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0],
                  [0.0, 0.0, 1.0]]
        super().__init__(program_id, vertices, colors, GL_LINES, location)
