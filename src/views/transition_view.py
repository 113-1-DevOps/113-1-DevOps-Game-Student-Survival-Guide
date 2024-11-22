<<<<<<< HEAD
import pygame
from config.constants import *
from utils.ui_tool import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class TransitionView:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load("images/transitions/transition_heart_full.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_position = (0, 0)
        self.button = pygame.image.load("images/transitions/transition_button.png")
        # 下一關卡的按鈕的位置
        self.button_position = center_to_top_left(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
            self.button.get_width(), self.button.get_height()
        )
        self.button_rect = self.button.get_rect(topleft=self.button_position)

    def draw(self):
        screen.fill(pygame.Color('white'))
        screen.blit(self.background, self.background_position)
        screen.blit(self.button, self.button_position)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.button_rect.collidepoint(event.pos):
            return TRANSITION
        return None
=======

>>>>>>> d2edee631c3e369693b8f9af4321532540042938
