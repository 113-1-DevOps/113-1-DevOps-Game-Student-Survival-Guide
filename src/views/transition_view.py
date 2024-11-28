import pygame
from config.constants import *
from utils.ui_tool import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class TransitionView:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load("images/transitions/transition_heart_full.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_position = (0, 0)
        self.button = pygame.image.load("images/transitions/transition_button.png")
        button_width = self.button.get_width() * 0.9
        button_height = self.button.get_height() * 0.9
        self.button = pygame.transform.scale(self.button, (button_width,button_height))

        # 下一關卡的按鈕的位置, test01
        self.button_position = center_to_top_left(
            0.7 * SCREEN_WIDTH , 0.55 * SCREEN_HEIGHT ,
            button_width, button_height
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
