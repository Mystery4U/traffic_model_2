from scipy.spatial import distance
from collections import deque


class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.vehicles = deque()
        self.road_properties()

    def road_properties(self):
        self.length = self.end-self.start

    def update(self, dt):
        n = len(self.vehicles)

        # Itereren over de auto's in de lijst (en de index meenemen)
        for index, vehicle in enumerate(self.vehicles):
            vehicle_left_back, vehicle_left_front, vehicle_right_back, vehicle_right_front = True, True, True, True
            lead = None
            # Create the index for iterating to the left and right
            left_index = index + 1
            right_index = index - 1

            # Deze voorwaarde is er zodat er altijd een element links zit totdat er een is gevonden
            while left_index < len(self.vehicles) and (vehicle_left_back is True or vehicle_right_back is True):
                # Itereren over de auto's links van de huidige auto
                left_element = self.vehicles[left_index]

                if vehicle_left_back is True:
                    if left_element.rijbaan == vehicle.rijbaan + 1 and abs(left_element.x - vehicle.x) < left_element.v * left_element.t:
                        vehicle_left_back = False

                if vehicle_right_back is True:
                    if left_element.rijbaan == vehicle.rijbaan - 1 and abs(left_element.x - vehicle.x) < left_element.v * left_element.t:
                        vehicle_right_back = False
                    else: pass

                left_index += 1

            # Deze voorwaarde is er zodat er altijd een element rechts zit totdat er een is gevonden
            while right_index >= 0 and (vehicle_left_front is True or vehicle_right_front is True):
                # Itereren over de auto's rechts van de huidige auto
                right_element = self.vehicles[right_index]

                if vehicle_left_front is True:
                    if right_element.rijbaan == vehicle.rijbaan + 1 and abs(right_element.x - vehicle.x) < vehicle.v * right_element.t:
                        vehicle_left_front = False
                    else: pass

                if lead is None and right_element.rijbaan == vehicle.rijbaan:
                    lead = right_element

                if vehicle_right_front is True:
                    if right_element.rijbaan == vehicle.rijbaan - 1 and abs(right_element.x - vehicle.x) < vehicle.v * right_element.t:
                        vehicle_right_front = False
                    else: pass

                right_index -= 1
            # -----------------------------------------------------------------------------------------
            if vehicle_left_back == True and vehicle_left_front == True:
                vehicle.links = True

            if vehicle_right_back == True and vehicle_right_front == True:
                vehicle.rechts = True

            self.vehicles[index].update(lead, dt)

        # for i in self.vehicles:
        #     print(i.rijbaan, i.x, i.v, i.links, i.rechts)
        # print('----------')