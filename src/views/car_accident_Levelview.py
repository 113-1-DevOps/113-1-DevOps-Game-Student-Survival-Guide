import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

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

        self.school_image = self.model.school_image  # 使用模型中已缩放的学校图像
        self.school_width = self.model.school_width
        self.school_height = self.model.school_height

        self.icon_scale_factor = 0.3  # 缩小图标尺寸
        self.font = pygame.font.Font(None, 24)  # 缩小字体大小

        self.gas_station_icon = pygame.image.load("images/car_accident/car_accident_gas_quantity.png").convert_alpha()
        self.gas_station_icon = pygame.transform.scale(
            self.gas_station_icon,
            (
                int(self.gas_station_icon.get_width() * self.icon_scale_factor),
                int(self.gas_station_icon.get_height() * self.icon_scale_factor)
            )
        )

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill((0, 0, 0))  # 清除屏幕内容

        # 绘制背景
        self.bg_y += self.bg_speed
        if self.bg_y >= SCREEN_HEIGHT:
            self.bg_y = 0

        background_x = (SCREEN_WIDTH - self.background.get_width()) // 2

        self.screen.blit(self.background, (background_x, self.bg_y - SCREEN_HEIGHT))
        self.screen.blit(self.background, (background_x, self.bg_y))

        # 绘制学校
        if self.model.school_visible:
            # 计算进度，从0到1
            progress = (self.model.school_appear_distance - self.model.distance_to_goal) / self.model.school_appear_distance
            progress = max(0, min(progress, 1))  # 确保进度在0到1之间

            # 计算要显示的学校图像高度
            school_height_cropped = int(self.school_height * progress)
            if school_height_cropped > 0:
                # 从底部开始裁剪学校图像
                school_image_cropped = self.school_image.subsurface(
                    pygame.Rect(
                        0,
                        self.school_height - school_height_cropped,
                        self.school_width,
                        school_height_cropped
                    )
                )
                # 学校水平居中，底部对齐屏幕顶部
                school_x = (SCREEN_WIDTH - self.school_width) // 2
                school_y = 0  # 学校的底部与屏幕顶部对齐
                self.screen.blit(school_image_cropped, (school_x, school_y))

        # 绘制障碍物和油桶（如果学校不可见）
        if not self.model.school_visible:
            for obstacle in self.model.obstacles:
                obstacle_image = self.obstacle_images[obstacle.type]
                obstacle_rect = obstacle_image.get_rect(center=(obstacle.x, obstacle.y))
                self.screen.blit(obstacle_image, obstacle_rect)

            for oil_drum in self.model.oil_drums:
                oil_drum_rect = self.oil_drum_image.get_rect(center=(oil_drum.x, oil_drum.y))
                self.screen.blit(self.oil_drum_image, oil_drum_rect)

        # 绘制玩家
        player_rect = self.player_image.get_rect(center=(self.model.player_x, self.model.player_y))
        self.screen.blit(self.player_image, player_rect)

        # 绘制油量
        fuel_text = f"{int(self.model.fuel)}%"
        fuel_surface = self.font.render(fuel_text, True, pygame.Color("white"))
        icon_x = SCREEN_WIDTH - self.gas_station_icon.get_width() - 10
        icon_y = 10
        self.screen.blit(self.gas_station_icon, (icon_x, icon_y))
        self.screen.blit(
            fuel_surface,
            (
                icon_x - fuel_surface.get_width() - 5,
                icon_y + (self.gas_station_icon.get_height() - fuel_surface.get_height()) // 2
            )
        )

        # 绘制距离
        distance_text = f"{int(self.model.distance_to_goal)} m"
        distance_surface = self.font.render(distance_text, True, pygame.Color("yellow"))
        distance_x = SCREEN_WIDTH - distance_surface.get_width() - 60
        distance_y = icon_y + self.gas_station_icon.get_height() + 5  # 缩小间距
        self.screen.blit(distance_surface, (distance_x, distance_y))

        pygame.display.flip()
