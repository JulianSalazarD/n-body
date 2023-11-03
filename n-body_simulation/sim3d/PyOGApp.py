from pygame.locals import *
from .camera import *
import os


class PyOGApp:
    def __init__(self, screen_posX, screen_posY, screen_width, screen_height):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()

        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Simulation')
        self.camera = None
        self.program_id = None
        self.clock = pygame.time.Clock()

        # limits
        self.min_x = -2500
        self.max_x = 2500
        self.min_y = -2500
        self.max_y = 2500
        self.min_z = -2500
        self.max_z = 2500

    def map_position(self, x, y, z):
        # relative position to the screen
        mapped_x = (x / self.screen_width) * (self.max_x - self.min_x) + self.min_x
        mapped_y = (y / self.screen_height) * (self.max_y - self.min_y) + self.min_y
        mapped_z = (z / self.screen_width) * (self.max_z - self.min_z) + self.min_z
        return mapped_x, mapped_y, mapped_z

    def initialise(self):
        pass

    def display(self):
        pass

    def camera_init(self):
        pass

    def mainloop(self):
        done = False
        self.initialise()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
            self.camera_init()
            self.display()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()
