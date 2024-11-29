import pygame
import random
from utils.ui_tool import scale_image
from config.constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class TyphoonView:
    def __init__(self, model):
        self.model = model
        self.background_image = None
        self.bg_y1 = 0
        self.bg_y2 = -SCREEN_HEIGHT

        self.player_images = {
            'left': scale_image(pygame.image.load("images/typhoon/typhoon_player_left.png"), 0.1, 0.2),
            'right': scale_image(pygame.image.load("images/typhoon/typhoon_player_right.png"), 0.1, 0.2),
        }
        self.button_images = {
            'left': scale_image(pygame.image.load("images/typhoon/typhoon_button_umb_left.png"), 0.1, 0.1),
            'right': scale_image(pygame.image.load("images/typhoon/typhoon_button_umb_right.png"), 0.1, 0.1),
        }
        self.weathercock_images = {
            'left': scale_image(pygame.image.load("images/typhoon/typhoon_weathercock_left.png"), 0.1, 0.1),
            'right': scale_image(pygame.image.load("images/typhoon/typhoon_weathercock_right.png"), 0.1, 0.1),
        }
        self.obstacle_images = [
            scale_image(pygame.image.load(f"images/typhoon/obstacle_{i:02}.png"), 0.5, 0.5)
            for i in range(1, 4)
        ]

        self.player_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5]
        self.button_positions = {
            'left': (SCREEN_WIDTH * 1 / 10, SCREEN_HEIGHT * 9 / 10),
            'right': (SCREEN_WIDTH * 9 / 10 - self.button_images['right'].get_width(), SCREEN_HEIGHT * 9 / 10),
        }
        self.weathercock_positions = {
            'left': (10, 10),
            'right': (SCREEN_WIDTH - self.weathercock_images['right'].get_width() - 10, 10),
        }

        self.load_background_image()

    def load_background_image(self):
        if self.background_image is None:
            original_image = pygame.image.load("images/typhoon/typhoon_background_2.png")
            self.background_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update_background(self, speed):
        self.bg_y1 += speed
        self.bg_y2 += speed

        if self.bg_y1 >= SCREEN_HEIGHT:
            self.bg_y1 = self.bg_y2 - SCREEN_HEIGHT
        if self.bg_y2 >= SCREEN_HEIGHT:
            self.bg_y2 = self.bg_y1 - SCREEN_HEIGHT

    def draw(self, elapsed_time):
        screen = pygame.display.get_surface()

        # 更新背景位置以實現滾動效果
        self.update_background(2)  # 調整背景的下落速度

        # 畫出背景
        screen.blit(self.background_image, (0, self.bg_y1))
        screen.blit(self.background_image, (0, self.bg_y2))

        # 畫風向指示
        if self.model.wind_direction == 'LEFT':
            screen.blit(self.weathercock_images['left'], self.weathercock_positions['left'])
        else:
            screen.blit(self.weathercock_images['right'], self.weathercock_positions['right'])

        # 畫雨傘按鈕
        screen.blit(self.button_images['left'], self.button_positions['left'])
        screen.blit(self.button_images['right'], self.button_positions['right'])

        # 畫玩家
        player_image = self.player_images['left'] if self.model.umbrella_direction == 'LEFT' else self.player_images['right']
        screen.blit(player_image, (self.model.player_pos[0], self.model.player_pos[1]))

        # 畫障礙物
        for obstacle in self.model.obstacles:
            obstacle_image = obstacle[2]
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # 畫存活時間
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {int(elapsed_time)}", True, pygame.Color('black'))
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - 50, 10))

        pygame.display.flip()
