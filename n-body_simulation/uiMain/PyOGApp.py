from pygame.locals import *
from sim3d.camera import *
import os


# configuracion pantall modelo 3d
class PyOGApp:
    def __init__(self, screen_width, screen_height):
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

    def initialise(self):
        pass

    def display(self):
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
                    if event.key == K_RETURN:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.view_scale(1)
                    if keys[pygame.K_DOWN]:
                        self.view_scale(0)
                    if keys[pygame.K_RIGHT]:
                        self.update_speed(1)
                    if keys[pygame.K_LEFT]:
                        self.update_speed(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.view_scale(1)
                    elif event.button == 5:
                        self.view_scale(0)

            self.display()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def view_scale(self, i):
        pass

    @classmethod
    def update_speed(cls, i):
        pass
