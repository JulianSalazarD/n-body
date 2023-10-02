import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from uiMain.Camera import Camera


class UiMain:
    def __init__(self, screen_width, screen_height, minimus, maximus):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = (0, 0, 0, 1)
        self.drawing_color = (1, 1, 1, 1)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('OpenGL in Python')
        self.done = False
        self.minimus = minimus
        self.maximus = maximus
        self.camera = Camera()
        self.mainloop()

    def initialise(self):
        glClearColor(self.background_color[0], self.background_color[1], self.background_color[2],
                     self.background_color[3])
        glColor(self.drawing_color)

        # projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.minimus, self.maximus, self.minimus, self.maximus, self.minimus, self.maximus)
        # gluPerspective(60, (self.screen_width / self.screen_height), 0.1, 1000.0)

    def camera_init(self):
        # modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, self.screen.get_width(), self.screen.get_height())
        glEnable(GL_DEPTH_TEST)
        self.camera.update(self.screen.get_width(), self.screen.get_height())

    def draw_world_axes(self):
        glLineWidth(4)
        glBegin(GL_LINES)
        glColor(1, 0, 0)
        glVertex3d(self.minimus, 0, 0)
        glVertex3d(self.maximus, 0, 0)
        glColor(0, 1, 0)
        glVertex3d(0, self.minimus, 0)
        glVertex3d(0, self.maximus, 0)
        glColor(0, 0, 1)
        glVertex3d(0, 0, self.minimus)
        glVertex3d(0, 0, self.maximus)
        glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera_init()
        self.draw_world_axes()

    def mainloop(self):
        self.initialise()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
            self.display()
            pygame.display.flip()
        pygame.quit()
