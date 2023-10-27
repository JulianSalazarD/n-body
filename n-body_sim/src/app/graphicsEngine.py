from OpenGL.GL import *
import numpy as np
import pyrr
from OpenGL.GL.shaders import compileProgram, compileShader

from src.app.Material import Material
from src.app.PointLight import PointLight
from src.app.camera import Camera
from src.app.entity import Entity
from src.app.mesh import Mesh

ENTITY_TYPE = {
    "SPHERE": 0,
    "POINTLIGHT": 1,
}

UNIFORM_TYPE = {
    "MODEL": 0,
    "VIEW": 1,
    "PROJECTION": 2,
    "CAMERA_POS": 3,
    "LIGHT_COLOR": 4,
    "LIGHT_POS": 5,
    "LIGHT_STRENGTH": 6,
}


class GraphicsEngine:
    """
        Draws entities and stuff.
    """
    __slots__ = (
        "meshes", "materials", "shader",
        "uniform_locations", "light_locations")

    def __init__(self):
        """
            Initializes the rendering system.
        """

        self._set_up_opengl()

        self._create_assets()

        self._set_onetime_uniforms()

        self._get_uniform_locations()

    def _set_up_opengl(self) -> None:
        """
            Configure any desired OpenGL options
        """

        glClearColor(0.0, 0.0, 0.0, 1)
        glEnable(GL_DEPTH_TEST)

    def _create_assets(self) -> None:
        """
            Create all of the assets needed for drawing.
        """

        self.meshes: dict[int, Mesh] = {
            ENTITY_TYPE["SPHERE"]: Mesh("src/app/models/sphere.obj"),
        }
        self.materials: dict[int, Material] = {
            ENTITY_TYPE["SPHERE"]: Material("src/app/gfx/img_1.png"),
        }

        self.shader = GraphicsEngine.create_shader(
            vertex_filepath="src/app/shaders/vertex.txt",
            fragment_filepath="src/app/shaders/fragment.txt")

    def _set_onetime_uniforms(self) -> None:
        """
            Some shader data only needs to be set once.
        """

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=10, far=10000, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

    def _get_uniform_locations(self) -> None:
        """
            Query and store the locations of shader uniforms
        """

        glUseProgram(self.shader)
        self.uniform_locations: dict[int, int] = {
            UNIFORM_TYPE["CAMERA_POS"]: glGetUniformLocation(
                self.shader, "cameraPosition"),
            UNIFORM_TYPE["MODEL"]: glGetUniformLocation(self.shader, "model"),
            UNIFORM_TYPE["VIEW"]: glGetUniformLocation(self.shader, "view"),
        }

        self.light_locations: dict[int, list[int]] = {
            UNIFORM_TYPE["LIGHT_COLOR"]: [
                glGetUniformLocation(self.shader, f"Lights[{i}].color")
                for i in range(8)
            ],
            UNIFORM_TYPE["LIGHT_POS"]: [
                glGetUniformLocation(self.shader, f"Lights[{i}].position")
                for i in range(8)
            ],
            UNIFORM_TYPE["LIGHT_STRENGTH"]: [
                glGetUniformLocation(self.shader, f"Lights[{i}].strength")
                for i in range(8)
            ],
        }

    def render(self,
               camera: Camera, renderables: dict[int, list[Entity]]) -> None:
        """
            Draw everything.

            Parameters:

                camera: the scene's camera

                renderables: all the entities to draw
        """

        # refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        glUniformMatrix4fv(
            self.uniform_locations[UNIFORM_TYPE["VIEW"]],
            1, GL_FALSE, camera.get_view_transform())

        for i in range(len(renderables[ENTITY_TYPE["POINTLIGHT"]])):
            light: PointLight = renderables[ENTITY_TYPE["POINTLIGHT"]][i]

            glUniform3fv(
                self.light_locations[UNIFORM_TYPE["LIGHT_POS"]][i],
                1, light.position)
            glUniform3fv(
                self.light_locations[UNIFORM_TYPE["LIGHT_COLOR"]][i],
                1, light.color)
            glUniform1f(
                self.light_locations[UNIFORM_TYPE["LIGHT_STRENGTH"]][i],
                light.strength)

        glUniform3fv(self.uniform_locations[UNIFORM_TYPE["CAMERA_POS"]],
                     1, camera.position)

        for entity_type, entities in renderables.items():

            if entity_type not in self.meshes:
                continue

            mesh = self.meshes[entity_type]
            material = self.materials[entity_type]
            mesh.arm_for_drawing()
            material.use()
            for entity in entities:
                glUniformMatrix4fv(
                    self.uniform_locations[UNIFORM_TYPE["MODEL"]],
                    1, GL_FALSE, entity.get_model_transform())
                mesh.draw()

        glFlush()

    def destroy(self) -> None:
        """ free any allocated memory """

        for mesh in self.meshes.values():
            mesh.destroy()
        for material in self.materials.values():
            material.destroy()
        glDeleteProgram(self.shader)

    @staticmethod
    def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
        """
            Compile and link shader modules to make a shader program.

            Parameters:

                vertex_filepath: path to the text file storing the vertex
                                source code

                fragment_filepath: path to the text file storing the
                                    fragment source code

            Returns:

                A handle to the created shader program
        """

        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader
