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

    def update(self, dt): # Idea: sort vehicles on x value each update (done) and then assign lead/tail to them,
        n = len(self.vehicles)

        if n == 1:
            self.vehicles[0].update(None, None, dt)

        elif n == 2:
            lead = self.vehicles[0]
            tail = self.vehicles[1]
            self.vehicles[0].update(None, tail, dt)
            self.vehicles[1].update(lead, None, dt)

        elif n > 2:
            for i in range(0, n):
                if i == 0:
                    tail = self.vehicles[i+1]
                    self.vehicles[i].update(None, tail, dt)
                elif i == n-1:
                    lead = self.vehicles[i-1]
                    self.vehicles[i].update(lead, None, dt)
                else:
                    tail = self.vehicles[i+1]
                    lead = self.vehicles[i-1]
                    self.vehicles[i].update(lead, tail, dt)
