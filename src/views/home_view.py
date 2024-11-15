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
        # 開始按鈕的位置
        self.start_button_position = center_to_top_left(
            2 * SCREEN_WIDTH / 3, 2 * SCREEN_HEIGHT / 3, #中心點 x,y
            self.start_button.get_width(), self.start_button.get_height()
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
