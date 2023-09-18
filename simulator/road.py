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

        autos_links = []
        autos_rechts = []
        for auto in self.vehicles:
            if auto.y == 900/2 -50:
                autos_links.append(auto)
            else:
                autos_rechts.append(auto)
        if n== 1:
            self.vehicles[0].update(None,None,dt)
        elif n == 2:
            tail = self.vehicles[1]
            lead = self.vehicles[0]
            self.vehicles[0].update(None, tail, dt)
            self.vehicles[1].update(lead, None, dt)
            print("hoi 2 autos")
        else:
            for i in range(2, len(self.vehicles)+1):
                print(i)
                for j in range(1, len(self.vehicles)-i+1):
                    print(i,j)
                    if self.vehicles[-i].y == self.vehicles[-i - j].y:
                        lead = self.vehicles[-i - j]
                        for k in range(1,i):
                            if self.vehicles[-i].y != self.vehicles[-i + k].y:
                                tail = self.vehicles[-i+k]
                                self.vehicles[-i].update(lead,tail,dt)
                                print(lead,tail)
                            else:
                                self.vehicles[-i].update(lead, None, dt)
                    else:
                        self.vehicles[-i].update(None, None, dt)



            # for j in range(1, len(self.vehicles)-i):
            #     if len(autos_links) > 0 and self.vehicles[-i].y == self.vehicles[-i-j].y:
            #         lead = self.vehicles[-i-j]
            #         self.vehicles[i].update(lead, None, 0)
            #         break
            #     elif len(autos_rechts) > 0 and self.vehicles[-i].y == self.vehicles[-i-j].y:
            #         lead = self.vehicles[-i-j]
            #         self.vehicles[i].update(lead, None, 0)
            #         break
            #     if len(autos_links) > 0 and self.vehicles[i].y != self.vehicles[i+j].y:
            #         tail = self.vehicles[i+j]
            #         self.vehicles[i].update(None, tail, 0)
            #         break

            #
            #     elif len(autos_rechts) > 0 and self.vehicles[i].y != self.vehicles[i+j].y:
            #         tail = self.vehicles[i+j]
            #         self.vehicles[i].update(None, tail, 0)
            #         break

