import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .road import Road
from .vehicle_generator import VehicleGenerator
from collections import deque


class Simulation:
    def __init__(self, config={}):
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60         # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.time_travel = []
        self.index = 0

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def update(self):
        for road in self.roads:
            road.vehicles = deque(sorted(road.vehicles, key=lambda obj: obj.x, reverse=True)) # Sorteer vehicles deque op x-waarde

            for i in road.vehicles:
                # print(vars(i))
                break

            if len(road.vehicles) == 0:
                continue

            vehicle = road.vehicles[0]
            if vehicle.x >= road.length:
                road.vehicles.popleft()
                self.index += 1
                print(self.index)
                self.time_travel.append(self.t - vehicle.time_added)  # Append the current time_travel data
                if self.index == 50:
                    plt.hist(self.time_travel, bins=10, edgecolor='black')
                    plt.xlabel('Values')
                    plt.ylabel('Frequency')
                    plt.title('Histogram of Values')
                    plt.show()

            road.update(self.dt)

        for gen in self.generators:
            gen.update()

        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
