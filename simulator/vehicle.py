import numpy as np
import itertools
import math
from decimal import Decimal
from collections import deque
from .road import Road
from .window import Window

class Vehicle:
    def __init__(self, sim, config={}):
        self.set_default_config()
        self.car_type()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.l= 4
        self.b = 2.2 * 20       # 2.2m with a factor 20 to make it look good on screen
        self.s0 = 2000            # Als er een nieuwe auto ingevoegd moet worden dan moet daar minimaal 50 meter tussen zitten
        self.v_max = 100/3.6    # Er geldt een maximale snelheid van 100 km/h
        self.x = 0              # Auto's beginnen op x=0
        self.rijbaan = 1        # Rijbaan indexwaarde
        self.rechts = False
        self.links = False
        self.v = self.v_max     # Auto's beginnen met 100 km/h
        self.t = 2              # Tijd tussen de auto's (hou minimaal 2s afstand)

    def car_type(self):
        if np.random.choice([0, 1], 1, p=[0.95, 0.05]) == 0:
            self.type = 0
        else:
            self.type = 1

    def update(self, lead, dt):
        factor = 1/3.6

        # Voor de eerste auto in de rij
        if lead is None:
            # 80 - 95 - 110
            if self.v < self.v_max - (20 + ((self.rijbaan - 1) * 15)) * factor:
                self.v += 1 * factor
            # 100 - 120 - 140
            elif self.v > self.v_max + ((self.rijbaan - 1) * 20) * factor:
                self.v -= 1 * factor
            else:
                self.v += np.random.choice([1 * factor, 0, -1 * factor])
        # -------------------------------
        elif lead is not None:
            if abs(lead.x - self.x) < self.v * self.t:
                if self.links == True and self.rijbaan != 2:
                    self.rijbaan += 1
                    self.v += 1 * factor
                    self.links = False
                    self.rechts = False
                else:
                    self.v = lead.v - (2 * factor)
            else:
                # 80 - 90
                if self.v < self.v_max - (20 + (self.rijbaan - 1) * 10) * factor:
                    self.v += 1 * factor
                # 100 - 120
                elif self.v > self.v_max + ((self.rijbaan - 1) * 20) * factor:
                    self.v -= 1 * factor
                else:
                    self.v += np.random.choice([1 * factor, 0, -1 * factor])

        if self.rechts == True and self.rijbaan != 1:
            self.rijbaan -= 1
            self.v -= 1 * factor
            self.rechts = False
            self.links = False

        self.x = (self.x + (self.v * dt))
