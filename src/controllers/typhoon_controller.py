import pygame
from config.constants import *
from models.typhoon_level_model import TyphoonModel
from views.typhoon_view import TyphoonView

class TyphoonController:
    def __init__(self):
        self.model = TyphoonModel()
        self.view = TyphoonView(self.model)

    def start(self):
        clock = pygame.time.Clock()
        running = True
        start_time = pygame.time.get_ticks()

        while running:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed_time >= 30:
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.view.button_positions['left'][0] <= mouse_pos[0] <= self.view.button_positions['left'][0] + self.view.button_images['left'].get_width():
                        if self.view.button_positions['left'][1] <= mouse_pos[1] <= self.view.button_positions['left'][1] + self.view.button_images['left'].get_height():
                            self.model.change_umbrella_direction(self.view.button_positions['left'])
                    if self.view.button_positions['right'][0] <= mouse_pos[0] <= self.view.button_positions['right'][0] + self.view.button_images['right'].get_width():
                        if self.view.button_positions['right'][1] <= mouse_pos[1] <= self.view.button_positions['right'][1] + self.view.button_images['right'].get_height():
                            self.model.change_umbrella_direction(self.view.button_positions['right'])

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.model.move_player(-1)
            if keys[pygame.K_RIGHT]:
                self.model.move_player(1)

            self.model.update()
            if self.model.check_collision():
                return False

            self.view.draw(elapsed_time)
            clock.tick(60)
