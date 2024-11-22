
import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.ui_tool import center_to_top_left

class CarAccidentLevelView:
    def __init__(self, model):
        self.model = model

        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Display initialized with set_mode in CarAccidentLevelView.__init__()")

        self.background = pygame.image.load("images/car_accident/car_accident_background.png").convert_alpha()

        scale_factor_bg = SCREEN_HEIGHT / self.background.get_height()
        new_width = int(self.background.get_width() * scale_factor_bg)
        new_height = SCREEN_HEIGHT  
        self.background = pygame.transform.scale(self.background, (new_width, new_height))

        self.bg_y = 0  
        self.bg_speed = 2  
        self.school_visible = False  

        self.scale_factor = 0.4  

        self.player_image = pygame.image.load("images/car_accident/car_accident_player.png").convert_alpha()
        self.player_image = pygame.transform.scale(
            self.player_image,
            (int(self.player_image.get_width() * self.scale_factor), int(self.player_image.get_height() * self.scale_factor))
        )

        self.obstacle_images = [
            pygame.image.load("images/car_accident/car_accident_car_01.png").convert_alpha(),
            pygame.image.load("images/car_accident/car_accident_car_02.png").convert_alpha()
        ]
        self.obstacle_images = [
            pygame.transform.scale(img, (int(img.get_width() * self.scale_factor), int(img.get_height() * self.scale_factor)))
            for img in self.obstacle_images
        ]

        self.oil_drum_image = pygame.image.load("images/car_accident/car_accident_gas_barrel.png").convert_alpha()
        self.oil_drum_image = pygame.transform.scale(
            self.oil_drum_image,
            (int(self.oil_drum_image.get_width() * self.scale_factor), int(self.oil_drum_image.get_height() * self.scale_factor))
        )

        self.school_image = pygame.image.load("images/car_accident/car_accident_school.png").convert_alpha()
        self.school_image = pygame.transform.scale(
            self.school_image,
            (int(self.school_image.get_width() * self.scale_factor), int(self.school_image.get_height() * self.scale_factor))
        )

        self.gas_station_icon = pygame.image.load("images/car_accident/car_accident_gas_quantity.png").convert_alpha()
        self.gas_station_icon = pygame.transform.scale(
            self.gas_station_icon,
            (int(self.gas_station_icon.get_width() * self.scale_factor), int(self.gas_station_icon.get_height() * self.scale_factor))
        )

    def draw(self):
        """绘制游戏画面"""
        self.bg_y += self.bg_speed
        if self.bg_y >= SCREEN_HEIGHT:
            self.bg_y = 0

        background_x = (SCREEN_WIDTH - self.background.get_width()) // 2

        self.screen.blit(self.background, (background_x, self.bg_y - SCREEN_HEIGHT))
        self.screen.blit(self.background, (background_x, self.bg_y))

        player_rect = self.player_image.get_rect(center=(self.model.player_x, self.model.player_y))
        self.screen.blit(self.player_image, player_rect)

        for obstacle in self.model.obstacles:
            obstacle_image = self.obstacle_images[obstacle.type]
            obstacle_rect = obstacle_image.get_rect(center=(obstacle.x, obstacle.y))
            self.screen.blit(obstacle_image, obstacle_rect)

        for oil_drum in self.model.oil_drums:
            oil_drum_rect = self.oil_drum_image.get_rect(center=(oil_drum.x, oil_drum.y))
            self.screen.blit(self.oil_drum_image, oil_drum_rect)

        fuel_text = f"{int(self.model.fuel)}%"
        font = pygame.font.Font(None, 36)
        fuel_surface = font.render(fuel_text, True, pygame.Color("white"))
        self.screen.blit(self.gas_station_icon, (10, 10))  
        self.screen.blit(fuel_surface, (50, 10)) 

        distance_text = f"距离终点: {self.model.distance_to_goal} m"
        distance_surface = font.render(distance_text, True, pygame.Color("yellow"))
        self.screen.blit(distance_surface, (10, 50))  

        if self.model.distance_to_goal <= 200:
            self.school_visible = True
        if self.school_visible:
            progress = (200 - self.model.distance_to_goal) / 200
            school_y = progress * (SCREEN_HEIGHT - self.school_image.get_height())
            school_x = (SCREEN_WIDTH - self.school_image.get_width()) // 2
            self.screen.blit(self.school_image, (school_x, school_y))

        pygame.display.flip()
