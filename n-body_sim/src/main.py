import numpy as np
import scipy as sp


from src.app.app import App
from src.app.body import Body

SUN_MASS = 1.9891E30
SUN_RADIUS = 696340
EARTH_MASS = 5.972E24
EARTH_RADIUS = 6371

sun = Body(50, SUN_MASS, np.array([0., 0., 0.]), np.array([0., 0., 0.]))
earth = Body(30, EARTH_MASS, np.array([0., 0., sp.constants.astronomical_unit]),
             np.array([0., 2.9E4, 0.]))
jupyter = Body(40, 1.898E27, np.array([-5.0 * sp.constants.astronomical_unit, 0., 0.]),
               np.array([0., -1.3E4, 0.]))

if __name__ == '__main__':
    my_app = App([sun, earth])
    my_app.run()
    my_app.quit()

