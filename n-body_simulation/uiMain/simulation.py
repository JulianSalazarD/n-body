import scipy as sp

from sim3d.Axes import *
from sim3d.LoadMesh import *
from sim3d.PyOGApp import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat; 
out vec3 color;

void main()
{
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
out vec4 frag_color;
void main(){
    frag_color = vec4(color, 1);
}
'''


class Projections(PyOGApp):
    SCALE = 50 / sp.constants.astronomical_unit

    def __init__(self, data, data_color):
        super().__init__(1000, 700)
        self.axes = None
        self.teapot = None
        self.data = data
        self.data_color = data_color
        self.sphere = []
        self.positions = []
        self.max_r = 20
        self.min_r = 10

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)
        self.build_sphere()

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.axes.draw()
        for i in self.sphere:
            i.draw()
        self.update_position()
        self.update_window()
        # glLineWidth(1)

    def build_sphere(self):
        for i in range(len(self.data)):
            sc = self.data[i].radius
            position = self.data[i].position.copy() * Projections.SCALE
            self.positions.append(position)
            self.sphere.append(LoadMesh("models/sphere.obj", self.program_id,
                                        location=pygame.Vector3(position[0], position[1], position[2]),
                                        scale=pygame.Vector3(sc, sc, sc),
                                        move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)),
                                        color=self.data_color[i]))

    def update_position(self):
        for body in self.data:
            body.euler_method(self.data, 60. * 60. * 24)

    def update_window(self):
        for body in range(len(self.data)):
            self.positions[body] = self.data[body].position.copy() * Projections.SCALE
        for sphere in range(len(self.sphere)):
            self.sphere[sphere].set_move_translate(pygame.Vector3(self.positions[sphere][0],
                                                                  self.positions[sphere][1],
                                                                  self.positions[sphere][2]))
