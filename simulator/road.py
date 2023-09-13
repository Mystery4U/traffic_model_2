import itertools
from scipy.spatial import distance
from collections import deque


class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.vehicles = deque()
        self.road_properties()

    def road_properties(self):
        self.length = distance.euclidean(self.start, self.end)

    def update(self, dt):
        n = len(self.vehicles)
        if n > 0:
            self.vehicles[0].update(None, dt)
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)
