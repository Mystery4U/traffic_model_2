import numpy as np
import itertools
from collections import deque
from .road import Road


class Vehicle:
    def __init__(self, sim, config={}):
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        # self.init_properties()

    def set_default_config(self):
        self.l= 4
        self.s0 = 4
        self.v_max = 100
        self.x = 0
        self.y = 900/2 + 25
        self.v = self.v_max
        # self.d = 0

    # def init_properties(self):
    #     a=1

    def update(self, lead, dt):
        T = 1

        # Voor de eerste auto
        if lead is None:
            if self.v < self.v_max - 20:
                self.v += 1
            elif self.v > self.v_max + 5:
                self.v -= 1
            else:
                self.v += np.random.choice([1, -1])

        if lead is not None:
            if self.y == 900/2 + 25:
                if (lead.v-self.v) * T < 10 and self.y == lead.y:
                    self.y -= 75
                    self.v += 50
                    # self.d += 1

                elif self.v < 80:
                    self.v += 1
                elif self.v > 100:
                    self.v -= 1
                else:
                    self.v += np.random.choice([1, -1])

            elif self.y == 900/2 - 50:
                if (self.v-lead.v) * T > 1000:
                    self.y += 75
                    # self.d = -1
                else:
                    if self.v > lead.v:
                        self.v -= 1
                    elif self.v < 105:
                        self.v += 100
                    elif self.v > 1200:
                        self.v -= 1
                    else:
                        self.v += np.random.choice([1, -1])

            # elif self.d == 1 and self.y != 900/2 - 50:
            #     self.y -= 5
            #     self.v += 2
            #
            # elif self.d == -1 and self.y != 900/2 + 25:
            #     self.y += 5
            #     self.v -= 2

            else:
                pass
        else:
            pass

        self.x += self.v * dt
