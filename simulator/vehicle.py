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
        # self.r = False          # Mag naar rechts
        # self.l = False          # Mag naar links
        self.d = 0

    def car_type(self):
        if np.random.choice([0, 1], 1, p=[0.95, 0.05]) == 0:
            self.type = 0
        else:
            self.type = 1

    def update(self, lead, tail, dt):
        # Vrachtwagen
        if self.l == 19:
            # Rijdt standaard rechts
            self.y = 900/2 + 25
            # Haalt nooit in
            self.d = 0
        # --------------------------------
        # Smooth inhalen
        if self.d == 1 and self.l == 4:
            if self.y == 900/2 - 50:
                self.d = 0
            else:
                self.y -= 5
                self.v += 1/3.6

        if self.d == -1 and self.l == 4:
            if self.y == 900/2 + 25:
                self.d = 0
            else:
                self.y += 5
                self.v -= 1/3.6
        # ---------------------------------
        # Voor de eerste auto in de rij
        if lead is None:

            # Personenauto: bounded random walk tussen 80 en 120
            if self.y == 900/2 + 25 and self.l == 4:
                if self.v < self.v_max - 20/3.6:
                    self.v += 1/3.6
                elif self.v > self.v_max + 20/3.6:
                    self.v -= 1/3.6
                else:
                    self.v += np.random.choice([1/3.6, 0, -1/3.6])

            # Vrachtwagen: bounded random walk tussen 80 en 85
            elif self.y == 900/2 + 25 and self.l == 19:
                if self.v < 80/3.6:
                    self.v += 1/3.6
                elif self.v > 85/3.6:
                    self.v -= 1/3.6
                else:
                    self.v += np.random.choice([1/3.6, 0, -1/3.6])

            # Als de voorste auto links rijdt dan moet gaat die minimaal 120 km/h en naar rechts zodra de afstand met zijn tail groot genoeg is
            else:
                self.v = 120 / 3.6
                if abs(self.x - tail.x + ((self.l + tail.l) / 2)) > tail.v * self.t * 1.5 and self.l == 4:
                    self.y += 5
                    self.d = -1
                else:
                    pass
        # --------------------------------------------------------
        # Voor alle andere auto's (met dus minimaal een voorligger)
        elif lead is not None:
            # Als de auto rechts rijdt
            if self.y == 900/2 + 25:
                # Als de afstand tussen de auto en zijn voorligger kleiner is dat 2s en ze beide rechts zitten
                if abs(lead.x - self.x + ((self.l + lead.l) / 2)) < self.v * self.t and self.y == lead.y:
                    # Als er een achterligger is
                    if tail != None:
                        # Als de achterligger ver genoeg is en het is een personenauto ga dan naar links en versnel
                        if self.l == 4 and abs(tail.x - self.x + ((self.l + tail.l) / 2)) > tail.v * self.t:
                            self.y -= 5
                            self.v += 1 / 3.6
                            self.d = 1

                    # Als het een vrachtwagen is vertragen
                    if self.l == 19:
                        self.v -= 1 / 3.6

                if self.v < 80/3.6:   # Bounded random walk met 80 < v < 95
                    self.v += 2/3.6
                elif self.v > 95/3.6:
                    self.v -= 2/3.6
                else:
                    self.v += np.random.choice([3/3.6, -3/3.6])

            # Als de auto links rijdt
            elif self.y == 900/2 - 50:
                # Als de auto een achterligger heeft
                if tail != None:
                    # Als de afstand tussen de auto voor en achter groot genoeg is, ga naar rechts
                    if abs(self.x - lead.x + ((self.l + lead.l) / 2)) > self.v * self.t and (abs(self.x - tail.x) + (self.l + tail.l)) / 2 > tail.v * self.t and tail.y == lead.y == 900/2 + 25:
                        self.v += -2/3.6
                        self.y += 5
                        self.d = -1

                    # Als auto voor rechts rijdt en auto achter links rijdt en er is genoeg afstand met de auto voor, naar rechts
                    elif abs(self.x - lead.x + ((self.l + lead.l) / 2)) > self.v * self.t and lead.y == 900/2 + 25 and tail.y == 900/2 -50:
                        self.v += -2 / 3.6
                        self.y += 5
                        self.d = -1

                    # Auto voor en achter rijden ook links, dan altijd rechts
                    elif lead.y == tail.y == 900/2 - 50:
                        self.v += -2 / 3.6
                        self.y += 5
                        self.d = -1
                if self.v < 105/3.6:  # Bounded random walk met 105 < v < 120
                    self.v += 2/3.6
                elif self.v > 130/3.6:
                    self.v -= 2/3.6
                else:
                    self.v += np.random.choice([1/3.6, 0, -1/3.6])
            else:
                pass

        self.x = (self.x + (self.v * dt))
