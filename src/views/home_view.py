# home_view.py
import pygame
from config.constants import *
from utils.ui_tool import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HomeView:
    def __init__(self):
        self.background = pygame.image.load("images/frontpage/frontpage_background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = pygame.image.load("images/frontpage/frontpage_button.png")
        button_width = self.start_button.get_width() * 0.7
        button_height = self.start_button.get_height() * 0.7
        self.start_button = pygame.transform.scale(self.start_button, (button_width,button_height))

        # 開始按鈕的位置, test02
        self.start_button_position = center_to_top_left(
            0.59 * SCREEN_WIDTH , 0.71 * SCREEN_HEIGHT ,
            button_width, button_height
        )
        self.start_button_rect = self.start_button.get_rect(topleft=self.start_button_position)

    def draw(self):
        screen.fill(pygame.Color('white'))
        screen.blit(self.background, (0, 0))
        screen.blit(self.start_button, self.start_button_position)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def handle_event(self, event):
        """返回點擊按鈕的事件結果給 Controller"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.start_button_rect.collidepoint(event.pos):
            return START
        return None
