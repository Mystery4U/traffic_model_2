import pygame
import os
import numpy as np
import time
import simulator
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from pygame import gfxdraw
from .road import Road


class PauseButton(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, (0,0,0), (0, 0, 50, 50), 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

button_group = pygame.sprite.Group()
pause_button = PauseButton((100, 50))
button_group.add(pause_button)

class Window:
    def __init__(self, sim, config={}):
        self.sim = sim
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.width = 1500
        self.height = 900
        self.lane_width = 70
        self.lanes = len(self.sim.roads)
        self.grass_width = (self.height - (self.lane_width * self.lanes)) / 2

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
        frame_number = 0

        paused = False
        running = True
        while running:
            output_directory = "frames_output"
            frame_filename = os.path.join(output_directory, f"frame_{frame_number:04d}.png")
            pygame.image.save(self.screen, frame_filename)
            frame_number += 1

            if loop:
                loop(self.sim, paused)

            pygame.display.update()
            clock.tick(self.fps)

            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.rect.collidepoint(event.pos):
                        paused = not paused  # Toggle pause state

            if not paused:
                self.draw()


    def run(self, steps_per_update=1):
        def loop(sim, paused):
            sim.paused = paused
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
        lane_y = self.grass_width + (self.lane_width * self.lanes) - self.lane_width
        dashed_line_index = 1

        for road in self.sim.roads:
            pos = (road.start, lane_y)
            size = (self.width, self.lane_width)
            color = (0, 0, 0)
            color2 = (255, 255, 255)
            self.box(pos, size, color)

            if dashed_line_index < self.lanes:
                self.draw_line_dashed(color2, (0, lane_y), (self.width, lane_y), dash_length=5)

            lane_y -= self.lane_width
            dashed_line_index += 1

    def background(self, r, g, b):
        self.screen.fill((r, g, b))

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))

        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

    def draw_vehicle(self, vehicle, road, speed):
        # Plaatje voor de auto
        car = pygame.image.load(os.path.join('image/car.png'))
        width = car.get_rect().width
        height = car.get_rect().height
        car.convert()
        car = pygame.transform.scale(car, (width/20, height/3))

        # Zonder plaatje
        pos = vehicle.x * 1500/5000, self.grass_width + (self.lane_width * self.lanes) - (self.lane_width * vehicle.rijbaan) + (self.lane_width - vehicle.b) / 2
        cmap = plt.get_cmap('RdYlGn_r')
        norm = Normalize(vmin=70/3.6, vmax=120/3.6)
        normalized_value = norm(speed)
        rgba = cmap(normalized_value)
        r, g, b, _ = rgba
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        color = (r, g, b)

        for road in self.sim.roads:
            size = vehicle.l * (self.width/road.length), vehicle.b

        # For image of the car
        # if vehicle.type == 0:
            self.box(pos, size, color)
        # else:
        #     self.screen.blit(car, pos)

    def draw_vehicles(self):
        for road in self.sim.roads:
            for vehicle in road.vehicles:
                speed = vehicle.v
                self.draw_vehicle(vehicle, road, speed)


    def draw(self):
        self.background(*self.bg_color)
        self.draw_roads()
        self.draw_status()
        self.draw_vehicles()
        button_group.draw(self.screen)
