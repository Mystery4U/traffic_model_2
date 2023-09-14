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
        if n > 0:
            self.vehicles[0].update(None, None, dt)
            for i in range(1, n):
                lead = self.vehicles[i-1]
                # tail = self.vehicles[i]
                self.vehicles[i].update(lead, None, dt)

        # print(n)
        # print('---')

        # if n > 0:
        #     self.vehicles[0].update(None, None, dt)
        #     if n == 2:
        #         for i in range(0, n):
        #             lead = self.vehicles[i]
        #             tail = self.vehicles[i-1]
        #             self.vehicles[i].update(lead, tail, dt)
        #
        #     for i in range(0, n):
        #         if i == 0:
        #             lead = self.vehicles[i]
        #             print(lead.x)
        #             self.vehicles[i].update(lead, None, dt)
        #         elif i == n-1:
        #             lead = self.vehicles[i-1]
        #             print(lead.x)
        #             self.vehicles[i].update(lead, None, dt)
        #         else:
        #             lead = self.vehicles[i-1]
        #             tail = self.vehicles[i+1]
        #             print(lead.x)
        #             print(tail.x)
        #             self.vehicles[i].update(lead, tail, dt)

            # print('--------')

        # if n == 1:
        #     self.vehicles[0].update(None, None, dt)
        # elif n == 2:
        #     lead = self.vehicles[0]
        #     self.vehicles[1].update(lead, None, dt)
        # else:
        #     for i in range(1, n-1):
        #         lead = self.vehicles[i-1]
        #         tail = self.vehicles[i+1]
        #         self.vehicles[i].update(lead, tail, dt)
