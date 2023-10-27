from glapp.PyOGApp import *
from glapp.Axes import *
from glapp.LoadMesh import *

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
    def __init__(self, data):
        super().__init__(200, 20, 1000, 700)
        self.axes = None
        self.teapot = None
        self.data = data
        self.sphere = []
        self.positions = []

    def initialise(self):
        # glOrtho(-2500, 2500, -2500, 2500, -2500, 2500)
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)
        self.build_sphere()
        '''
        for i in range(10):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            z = random.randint(-250, 250)
            sc = random.randint(5, 20)
            self.sphere.append(LoadMesh("models/sphere.obj", self.program_id, location=pygame.Vector3(x, y, z),
                                        scale=pygame.Vector3(sc, sc, sc),
                               move_rotation=Rotation(1, pygame.Vector3(0, 1, 0))))
        '''

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
        # glLineWidth(5)

    def build_sphere(self):
        # min_radius = min(self.data, key=lambda body: body.radius).radius
        # max_radius = max(self.data, key=lambda body: body.radius).radius
        for body in self.data:
            # sc = ((body.radius - min_radius) * (5. - 4.)) / ((max_radius - min_radius) + 4.)
            sc = body.radius
            position = body.position.copy() / 1875e5
            self.positions.append(position)
            print(position, sc)
            self.sphere.append(LoadMesh("models/sphere.obj", self.program_id,
                                        location=pygame.Vector3(position[0], position[1], position[2]),
                                        scale=pygame.Vector3(sc, sc, sc),
                                        move_rotation=Rotation(1, pygame.Vector3(0, 1, 0))))

    def update_position(self):
        for body in self.data:
            body.euler_method(self.data, 60. * 60.)
            if body.radius == 30: print(body.position)

    def update_window(self):
        # for sphere in range(len(self.sphere)):
        #    self.sphere[sphere].set_move_translate(pygame.Vector3(-self.positions[sphere][0],
        # -self.positions[sphere][1],
        # -self.positions[sphere][2]))

        temp = self.positions.copy()
        for body in range(len(self.data)):
            #
            # self.positions[body] = -self.positions[body]
            # print(self.positions[body])
            self.positions[body] = self.data[body].position.copy() / 1875e5
        for sphere in range(len(self.sphere)):
            print(self.positions[sphere])
            self.sphere[sphere].set_move_translate(pygame.Vector3(temp[sphere][0] - self.positions[sphere][0],
                                                                  temp[sphere][1] - self.positions[sphere][1],
                                                                  temp[sphere][2] - self.positions[sphere][2]))
