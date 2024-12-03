import pygame
import random
from config.constants import *

class TyphoonModel:
    def __init__(self):
        self.player_pos = [SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT - 80]  # 將初始位置往上移動並向左移動10
        self.umbrella_direction = 'RIGHT'
        self.wind_direction = 'LEFT'
        self.last_wind_change = pygame.time.get_ticks()
        self.obstacles = []
        self.generate_obstacle_interval = 1000  # 每隔1秒生成障礙物
        self.last_obstacle_time = pygame.time.get_ticks()
        self.obstacle_images = [pygame.image.load(f"images/typhoon/obstacle_{i:02}.png") for i in range(1, 4)]
        self.lane_width = SCREEN_WIDTH // 10  # 調整軌道寬度，使其更緊密
        self.move_speed = 4  # 調整角色的移動速度，使其更快
        self.lane_start_x = (SCREEN_WIDTH - (self.lane_width * 5)) // 2 - 10  # 水平置中並向左移動10

    def move_player(self, direction):
        self.player_pos[0] += direction * self.move_speed  # 調整移動速度
        # 確保人物只能在軌道範圍內移動
        self.player_pos[0] = max(self.lane_start_x, min(self.lane_start_x + self.lane_width * 5 - self.lane_width, self.player_pos[0]))

    def change_umbrella_direction(self, pos):
        if pos[0] < SCREEN_WIDTH // 2:
            self.umbrella_direction = 'LEFT'
        else:
            self.umbrella_direction = 'RIGHT'

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_wind_change > 8000:
            self.wind_direction = random.choice(['LEFT', 'RIGHT'])
            self.last_wind_change = current_time

        # 當風向和雨傘方向相反時，角色會自動往雨傘的方向移動
        if self.umbrella_direction != self.wind_direction:
            self.player_pos[0] += self.move_speed if self.umbrella_direction == 'RIGHT' else -self.move_speed
            self.player_pos[0] = max(self.lane_start_x, min(self.lane_start_x + self.lane_width * 5 - self.lane_width, self.player_pos[0]))

        if current_time - self.last_obstacle_time > self.generate_obstacle_interval:
            # 更新障礙物數量和位置
            num_obstacles = random.randint(1, 2)  # 確保每次生成的障礙物數量不超過2個
            new_obstacles = []

            for _ in range(num_obstacles):
                lane = random.randint(0, 4)
                obstacle_image = random.choice(self.obstacle_images)
                obstacle_image = pygame.transform.scale(obstacle_image, (self.lane_width, self.lane_width))
                obstacle_x = self.lane_start_x + lane * self.lane_width + self.lane_width // 2

                # 檢查新障礙物的位置是否與現有障礙物重疊
                while any(abs(obstacle[0] - obstacle_x) < self.lane_width and abs(obstacle[1] - (-self.lane_width)) < self.lane_width for obstacle in self.obstacles + new_obstacles):
                    lane = random.randint(0, 4)
                    obstacle_x = self.lane_start_x + lane * self.lane_width + self.lane_width // 2

                new_obstacles.append([obstacle_x, -self.lane_width, obstacle_image])  # 初始位置在視窗上方

            self.obstacles.extend(new_obstacles)
            self.last_obstacle_time = current_time

        for obstacle in self.obstacles:
            obstacle[1] += 2  # 調整障礙物的下落速度

        self.obstacles = [ob for ob in self.obstacles if ob[1] < SCREEN_HEIGHT]

    def check_collision(self):
        for obstacle in self.obstacles:
            if abs(self.player_pos[0] - obstacle[0]) < 20 and self.player_pos[1] - obstacle[1] < 20:
                return True
        return False
