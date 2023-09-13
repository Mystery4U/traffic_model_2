import pygame
import numpy as np
from pygame import gfxdraw


class Window:
    def __init__(self, sim, config={}):
        self.sim = sim
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.width = 1500
        self.height = 900
        self.bg_color = (38, 82, 33)

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def loop(self, loop=None):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        clock = pygame.time.Clock()

        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        running = True
        while running:
            if loop:
                loop(self.sim)

            self.draw()

            pygame.display.update()
            clock.tick(self.fps)

            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False

    def run(self, steps_per_update=1):

        def loop(sim):
            sim.run(steps_per_update)

        self.loop(loop)

    def box(self, pos, size, color):
        x, y = pos
        l, h = size
        gfxdraw.box(self.screen, pygame.Rect(x, y, l, h), color)

    def draw_line_dashed(self, color, start_pos, end_pos, width=1, dash_length=10, exclude_corners=True):

        start_pos = np.array(start_pos)
        end_pos = np.array(end_pos)

        length = np.linalg.norm(end_pos - start_pos)

        dash_amount = int(length / dash_length)

        dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

        return [pygame.draw.line(self.screen, color, tuple(dash_knots[n]), tuple(dash_knots[n + 1]), width)
                for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

    def draw_roads(self):
        lanes = len(self.sim.roads) # 2
        lane_width = 70
        index = self.height/2

        for road in self.sim.roads:
            pos = (road.start, index)
            size = (road.length, lane_width)
            color = (0, 0, 0)
            color2 = (255, 255, 255)
            self.box(pos, size, color)
            self.draw_line_dashed(color2, (0, self.height/lanes), (self.width, self.height/lanes), dash_length=5)

            index -= 70

    def background(self, r, g, b):
        self.screen.fill((r, g, b))

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))

        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

    def draw_vehicle(self, vehicle, road):
        pos = vehicle.x, vehicle.y
        size = vehicle.l*10, 20
        color = (255, 255, 255)
        self.box(pos, size, color)

    def draw_vehicles(self):
        for road in self.sim.roads:
            for vehicle in road.vehicles:
                self.draw_vehicle(vehicle, road)

    def draw(self):
        self.background(*self.bg_color)
        self.draw_roads()
        self.draw_status()
        self.draw_vehicles()



