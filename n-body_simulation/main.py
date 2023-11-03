import numpy as np
import scipy as sp

from sim3d.body import Body
from uiMain.menu import Menu
from uiMain.simulation import Projections

SUN_MASS = 1.9891E30
SUN_RADIUS = 696340
EARTH_MASS = 5.972E24
EARTH_RADIUS = 6371

sun = Body(20, SUN_MASS, np.array([0., 0., 0.]), np.array([0., 0., 0.]))
earth = Body(15, EARTH_MASS, np.array([0., 0., sp.constants.astronomical_unit]),
             np.array([0., 2.9E4, 0.]))
jupyter = Body(18, 1.898E27, np.array([-5.0 * sp.constants.astronomical_unit, 0., 0.]),
               np.array([0., -1.3E4, 0.]))

mars = Body(16, 6.39 * 10 ** 23, np.array([-1.524 * sp.constants.astronomical_unit, 0., 0.]),
            np.array([0., 24.077 * 1000, 0.]))
mercury = Body(10, 3.30 * 10 ** 23, np.array([0.387 * sp.constants.astronomical_unit, 0., 0.]),
               np.array([0., -47.4 * 1000, 0.]))
venus = Body(12, 4.8685 * 10 ** 24, np.array([0.723 * sp.constants.astronomical_unit, 0., 0.]),
             np.array([0., -35.02 * 1000, 0.]))

if __name__ == '__main__':
    # Projections([sun, earth, jupyter, mars, mercury, venus]).mainloop()
    menu = Menu()
    menu.mainloop()
