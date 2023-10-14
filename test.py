import numpy as np
from simulator import *

sim = Simulation()

n = 2
d = {}
for x in range(0, n):
    d["lane_{}".format(x)] = (0, 5000)

lane_list = []
for key, value in d.items():
    exec(f'{key} = {value}')
    lane_list.append(eval(key))

sim.create_roads(lane_list)

sim.create_gen({
'vehicle_rate': 36,
'vehicles':[[3, {}], [3, {}]]})

win = Window(sim)
# win.zoom = 10
win.run(steps_per_update=5000)