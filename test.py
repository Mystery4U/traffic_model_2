from simulator import *

sim = Simulation()
lane_1 = (0, 5000)
lane_2 = (0, 5000)
sim.create_roads([lane_1, lane_2])

sim.create_gen({
'vehicle_rate': 60,
'vehicles':[[3, {}], [3, {}]]})

win = Window(sim)
win.zoom = 10
win.run(steps_per_update=1)
