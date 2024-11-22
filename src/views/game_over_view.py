import pygame
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.constants import *
from utils.ui_tool import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class GameOverView:
    def __init__(self):
        
        # 載入遊戲結束背景圖
        self.item = pygame.image.load("images/failpage/failpage_background.png")
        self.item = pygame.transform.scale(self.item, (SCREEN_WIDTH, SCREEN_HEIGHT))  
        self.original_item = self.item  # 保存原始圖片
        
        self.retry_button = pygame.image.load("images/failpage/failpage_button.png")
        self.retry_button_position = center_to_top_left(
            2 * SCREEN_WIDTH / 3, 2 * SCREEN_HEIGHT / 3, #中心點 x,y
            self.retry_button.get_width(), self.retry_button.get_height()
        )
        self.retry_button_rect = self.retry_button.get_rect(topleft=self.retry_button_position)

    def draw(self):
        scale_factor = 0.1  # 初始縮放比例
        scale_speed = 0.1  # 縮放速度
        while True:   
            if scale_factor < 1.0:  
                scale_factor += scale_speed
            else:
                break
            screen.fill((30, 49, 53))

            # 根據scale_factor進行單次縮放，保持比例
            new_width = int(self.original_item.get_width() * scale_factor)
            new_height = int(self.original_item.get_height() * scale_factor)
            self.item = pygame.transform.scale(self.original_item, (new_width, new_height))

            # 計算圖片的位置，使其居中顯示
            self.item_position = center_to_top_left(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.item.get_width(), self.item.get_height())

            screen.blit(self.item, self.item_position)
            pygame.display.flip()
            pygame.time.Clock().tick(10)
        screen.blit(self.retry_button, self.retry_button_position)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.retry_button_rect.collidepoint(event.pos):
            return RETRY
        return None        


if __name__ == '__main__':
    GameOverView().draw()
    