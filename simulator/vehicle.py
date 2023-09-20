import numpy as np
import itertools
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
        self.s0 = 50            # Als er een nieuwe auto ingevoegd moet worden dan moet daar minimaal 50 meter tussen zitten
        self.v_max = 100/3.6    # Er geldt een maximale snelheid van 100 km/h
        self.x = 0              # Auto's beginnen op x=0
        self.y = 900/2 + 25     # Auto's beginnen op de rechterbaan
        self.v = self.v_max     # Auto's beginnen met 100 km/h
        self.t = 2              # Tijd tussen de auto's (hou minimaal 2s afstand)
        self.r = False          # Mag naar rechts
        self.l = False          # Mag naar links

    def car_type(self):
        if np.random.choice([0, 1], 1, p=[0.95, 0.05]) == 0:
            self.type = 0
        else:
            self.type = 1

    def update(self, lead, tail, dt):
        if lead is None:    # Voor de eerste auto in de rij
            if self.y == 900/2 + 25:
                if self.v < self.v_max - 20/3.6:
                    self.v += 1
                elif self.v > self.v_max + 20/3.6:
                    self.v -= 1
                else:
                    self.v += np.random.choice([1/3.6, -1/3.6])
            else:
                self.v = 120 / 3.6
                if abs(self.x - tail.x) > tail.v * self.t * 1.5:
                    self.y += 75
                else:
                    pass

        elif lead is not None:    # Voor de andere auto's met voorliggers
            if self.y == 900/2 + 25:    # Als de auto rechts rijdt
                if abs(lead.x - self.x) < self.v * self.t and self.y == lead.y:   # Als de afstand tussen de auto en zijn voorligger kleiner is dat 2s en ze beide rechts zitten
                    self.y -= 75     # Ga naar de linkerbaan en verander je snelheid met 10 km/h
                    self.v += 10/3.6

                if self.v < 85/3.6:   # Bounded random walk met 80 < v < 95
                    self.v += 2/3.6
                elif self.v > 95/3.6:
                    self.v -= 2/3.6
                else:
                    self.v += np.random.choice([3/3.6, -3/3.6])

            elif self.y == 900/2 - 50:  # Als de auto links rijdt
                if abs(self.x - lead.x) < self.v * self.t and lead.y == 900/2 - 50:    # Als de voorganger ook links rijdt, hou afstand.
                    self.v += -2/3.6
                    self.y += 75

                if tail != None:
                    if abs(tail.x - self.x) > self.v * self.t and abs(lead.x-self.x) > self.v * self.t:
                        self.y += 75
                        self.v -= 5/3.6

                if self.v < 105/3.6:  # Bounded random walk met 105 < v < 120
                    self.v += 2/3.6
                elif self.v > 130/3.6:
                    self.v -= 2/3.6
                else:
                    self.v += np.random.choice([1/3.6, -1/3.6])
            else:
                pass

        self.x = (self.x + (self.v * dt))
