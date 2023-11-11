from .Mesh import *
from .Utils import *


# Cargar objeto 3d de un archivo
class LoadMesh(Mesh):

    def __init__(self, filename, program_id, draw_type=GL_TRIANGLES, location=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)), scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)), color=(1, 1, 1)):
        if color is None:
            color = []
        coordinates, triangles = self.load_drawing(filename)
        vertices = format_vertices(coordinates, triangles)
        colors = []
        for i in range(len(vertices)):
            colors.append(color[0])
            colors.append(color[1])
            colors.append(color[2])
        super().__init__(program_id, vertices, colors, draw_type, location, rotation, scale, move_rotation)

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == 'v ':
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == 'f ':
                    t1, t2, t3 = [value for value in line[2:].split()]
                    triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    triangles.append([int(value) for value in t3.split('/')][0] - 1)
                line = fp.readline()
        return vertices, triangles
