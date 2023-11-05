import numpy as np
from .vehicle import Vehicle


class VehicleGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.init_properties()

    def set_default_config(self):
        self.vehicle_rate = 20
        self.vehicles = [(1, {})]
        self.last_added_time = 0

    def init_properties(self):
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        total = sum(pair[0] for pair in self.vehicles)
        r = np.random.randint(1, total + 1)

        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                return Vehicle(config)

    def update(self):
        r = float(np.random.normal(60, 5, 1))
        if self.sim.t - self.last_added_time >= 60/r:
            road = self.sim.roads[0]
            if len(road.vehicles) == 0 or road.vehicles[-1].x > abs(self.upcoming_vehicle.v - road.vehicles[-1].v) * 2:
                self.upcoming_vehicle.time_added = self.sim.t
                if len(road.vehicles) != 0:
                    self.upcoming_vehicle.rijbaan = np.random.choice(list(range(1, len(self.sim.roads) + 1)))
                    # self.upcoming_vehicle.l = np.random.choice([4, 19], p=[0.9, 0.1])
                road.vehicles.append(self.upcoming_vehicle)

                # Reset last_added_time and upcoming_vehicle
                self.last_added_time = self.sim.t
            self.upcoming_vehicle = self.generate_vehicle()
