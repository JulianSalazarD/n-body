import tkinter as tk
from functools import partial
from tkinter import colorchooser

import numpy as np
import scipy as sp

from sim2d.body2 import Body2
from sim3d.body import Body
from uiMain.simulation import Projections
from uiMain.simulation2 import Simulation

AU = sp.constants.astronomical_unit
SUN_MASS = 1.9891E30
SUN_RADIUS = 696340
xVEL = 1000


class Menu(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.resizable(False, False)
        self.configure(bg="#F8883E")
        self.frame = None
        self.model = None
        self.n_bodies = None
        self.data = []
        self.modelo()
        self.default_data()
        self.color = None

    def modelo(self):
        self.clear_w()
        self.frame = tk.Frame(self, height=500, width=700)
        self.frame.place(x=150, y=100)
        self.frame.configure(bg="#18884A")
        tk.Button(self.frame, text="simulación 2D", command=self.simulation_2D, height=3, width=12).place(x=300, y=150)
        tk.Button(self.frame, text="simulación 3D", command=self.simulation_3D, height=3, width=12).place(x=300, y=250)

    def simulation_2D(self):
        self.model = "2D"
        self.cuerpos()

    def simulation_3D(self):
        self.model = "3D"
        self.cuerpos()

    def cuerpos(self):
        self.clear_w()
        self.frame = tk.Frame(self, height=500, width=700)
        self.frame.place(x=150, y=100)
        self.frame.configure(bg="#18884A")
        tk.Label(self.frame, text="Numero de cuerpos:", bg=self.frame["bg"],
                 font=("ROMAN", 15)).place(x=250, y=150)
        bodies = tk.Entry(self.frame)
        bodies.insert(0, "5")
        bodies.place(x=280, y=185)
        tk.Button(self.frame, text="back", command=self.modelo, height=2, width=5).place(x=10, y=450)
        tk.Button(self.frame, text="next", command=partial(self.get_body_numbers, bodies),
                  height=2, width=5).place(x=645, y=450)

    def get_body_numbers(self, bodies):
        self.n_bodies = int(bodies.get())
        self.planets_data(self.n_bodies)

    def planets_data(self, n_bodies):
        self.clear_w()
        i = self.n_bodies - n_bodies
        if i < self.n_bodies:
            self.configure_body_data(i)
        if i == self.n_bodies:
            self.confirm()

    def configure_body_data(self, i):
        self.frame = tk.Frame(self, height=500, width=800)
        self.frame.place(x=150, y=100)
        self.frame.configure(bg="#18884A")
        tk.Label(self.frame, text="Planet " + str(i + 1) + ":", bg=self.frame["bg"],
                 font=("Courier", 15)).place(x=250, y=10)

        # radius
        tk.Label(self.frame, text="radius: ", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=100, y=50)
        radius_entry = tk.Entry(self.frame)
        radius_entry.place(x=200, y=50)
        tk.Label(self.frame, text="xSolar Radius (696340 km)", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=450, y=50)

        # mass
        tk.Label(self.frame, text="Mass :", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=100, y=100)
        mass_entry = tk.Entry(self.frame)
        mass_entry.place(x=200, y=100)
        tk.Label(self.frame, text="xSolar masses (1.9891E30 kg)", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=450, y=100)

        # position
        tk.Label(self.frame, text="position :", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=100, y=150)
        posx_entry = tk.Entry(self.frame)
        posx_entry.place(x=200, y=150)
        posy_entry = tk.Entry(self.frame)
        posy_entry.place(x=200, y=170)
        posz_entry = tk.Entry(self.frame)
        posz_entry.place(x=200, y=190)
        tk.Label(self.frame, text="xAU (149 597 870 700 m)", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=450, y=170)

        # velocity
        tk.Label(self.frame, text="Velocity :", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=100, y=240)
        velx_entry = tk.Entry(self.frame)
        velx_entry.place(x=200, y=240)
        vely_entry = tk.Entry(self.frame)
        vely_entry.place(x=200, y=260)
        velz_entry = tk.Entry(self.frame)
        velz_entry.place(x=200, y=280)
        tk.Label(self.frame, text="x1000 m/s", bg=self.frame["bg"],
                 font=("Courier", 10)).place(x=450, y=260)

        # color
        color_button = tk.Button(self.frame, text="color", command=self.choose_color)
        color_button.place(x=200, y=350)
        self.color = tk.Frame(self.frame, height=20, width=20)
        self.color.place(x=450, y=350)
        self.color.configure(bg="#FFFFFF")
        if i < len(self.data):
            radius_entry.insert(0, str(self.data[i]["radius"]))
            mass_entry.insert(0, str(self.data[i]["mass"]))
            posx_entry.insert(0, str(self.data[i]["position"][0]))
            posy_entry.insert(0, str(self.data[i]["position"][1]))
            posz_entry.insert(0, str(self.data[i]["position"][2]))
            velx_entry.insert(0, str(self.data[i]["velocity"][0]))
            vely_entry.insert(0, str(self.data[i]["velocity"][1]))
            velz_entry.insert(0, str(self.data[i]["velocity"][2]))
            self.color.configure(bg=Menu.rgb_to_hex(self.data[i]["color"]))

        if self.model == "2D":
            posz_entry.config(state=tk.DISABLED)
            velz_entry.config(state=tk.DISABLED)

        planet_data = [radius_entry, mass_entry, (posx_entry, posy_entry, posz_entry),
                       (velx_entry, vely_entry, velz_entry)]

        tk.Button(self.frame, text="back", command=partial(self.get_back_data, i), height=2,
                  width=5).place(x=10, y=450)
        tk.Button(self.frame, text="next", command=partial(self.get_body_data, planet_data, i),
                  height=2, width=5).place(x=645, y=450)

    def get_back_data(self, i):
        if i == 0:
            self.init()
        self.planets_data(self.n_bodies - i + 1)

    def get_body_data(self, planet_data, i):
        body_data = {"radius": float(planet_data[0].get()),
                     "mass": float(planet_data[1].get()),
                     "position": (float(planet_data[2][0].get()),
                                  float(planet_data[2][1].get()),
                                  float(planet_data[2][2].get())),
                     "velocity": (float(planet_data[3][0].get()),
                                  float(planet_data[3][1].get()),
                                  float(planet_data[3][2].get())),
                     "color": Menu.hex_to_rgb(self.color["bg"])}
        if i < len(self.data):
            self.data[i] = body_data
        else:
            self.data.append(body_data)

        self.planets_data(self.n_bodies - i - 1)

    def confirm(self):
        self.clear_w()
        self.frame = tk.Frame(self, height=500, width=700)
        self.frame.place(x=150, y=100)
        self.frame.configure(bg="#18884A")
        tk.Button(self.frame, text="Confirm", command=self.start_simulation, height=3, width=12).place(x=300, y=150)
        tk.Button(self.frame, text="Cancel", command=self.init, height=3, width=12).place(x=300, y=250)

    def start_simulation(self):
        data = []
        r_max = max(self.data, key=lambda x: x["radius"])["radius"]
        r_min = min(self.data, key=lambda x: x["radius"])["radius"]

        if self.model == "3D":
            data_color = []
            for i in range(len(self.data)):
                self.data[i]["radius"] = ((self.data[i]["radius"] - r_min) / (r_max - r_min)) * (20-10) + 10
                print(self.data[i]["radius"])
                data.append(Body(self.data[i]["radius"],
                                 self.data[i]["mass"] * SUN_MASS,
                                 np.array([self.data[i]["position"][0] * AU,
                                           self.data[i]["position"][1] * AU,
                                           self.data[i]["position"][2] * AU]),
                                 np.array([self.data[i]["velocity"][0] * xVEL,
                                           self.data[i]["velocity"][1] * xVEL,
                                           self.data[i]["velocity"][2] * xVEL]))
                            )
                data_color.append((self.data[i]["color"][0] / 255,
                                   self.data[i]["color"][1] / 255,
                                   self.data[i]["color"][2] / 255))
            self.destroy()
            Projections(data, data_color).mainloop()

        else:
            for planet in self.data:
                planet["radius"] = ((planet["radius"] - r_min) / (r_max - r_min)) * (20 - 10) + 10
                print(planet["radius"])
                data.append(Body2(planet["radius"],
                                  planet["mass"] * SUN_MASS,
                                  np.array([planet["position"][0] * AU,
                                            planet["position"][1] * AU,
                                            planet["position"][2] * AU]),
                                  np.array([planet["velocity"][0] * xVEL,
                                            planet["velocity"][1] * xVEL,
                                            planet["velocity"][2] * xVEL]),
                                  planet["color"])
                            )
            self.destroy()
            Simulation(data).mainloop()

    def clear_w(self):
        for children in self.winfo_children():
            children.destroy()

    def default_data(self):
        # sun
        self.data.append({"radius": 1, "mass": 1, "position": (0, 0, 0), "velocity": (0, 0, 0), "color": (255, 255, 0)})
        # earth
        self.data.append({"radius": 6371/SUN_RADIUS, "mass": 5.972E24 / SUN_MASS, "position": (1, 0, 0),
                          "velocity": (0, 2.9E4 / xVEL, 0), "color": (0, 255, 255)})
        # mars
        self.data.append(
            {"radius": 3389.5 / SUN_RADIUS, "mass": 6.39 * 10 ** 23 / SUN_MASS, "position": (-1.524, 0, 0),
             "velocity": (0, 24.077, 0), "color": (223, 94, 41)})
        # mercury
        self.data.append(
            {"radius": 2440 / SUN_RADIUS, "mass": 3.30 * 10 ** 23 / SUN_MASS, "position": (0.387, 0, 0),
             "velocity": (0, -47.4, 0), "color": (156, 130, 114)})
        # venus
        self.data.append({"radius": 6051.8 / SUN_RADIUS, "mass": 4.8685 * 10 ** 24 / SUN_MASS, "position": (0.723, 0, 0),
                          "velocity": (0, -35.02, 0), "color": (215, 103, 83)})

    def init(self):
        self.clear_w()
        self.frame = None
        self.model = None
        self.n_bodies = None
        self.data = []
        self.modelo()
        self.default_data()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        self.color.configure(bg=color)

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb_color):
        return '#{:02X}{:02X}{:02X}'.format(rgb_color[0], rgb_color[1], rgb_color[2])
