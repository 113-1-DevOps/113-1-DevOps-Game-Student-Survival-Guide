import pygame
import random
from config.constants import *

class TyphoonModel:
    def __init__(self):
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50]
        self.umbrella_direction = 'RIGHT'
        self.wind_direction = 'LEFT'
        self.last_wind_change = pygame.time.get_ticks()
        self.obstacles = []
        self.generate_obstacle_interval = 1000  # 每隔1秒生成障礙物
        self.last_obstacle_time = pygame.time.get_ticks()
        self.obstacle_images = [pygame.image.load(f"images/typhoon/obstacle_{i:02}.png") for i in range(1, 4)]
        self.lane_width = (SCREEN_WIDTH - 200) // 5  # 設置軌道寬度
        self.move_speed = 5  # 調整角色的移動速度，使其更慢
        self.obstacle_size = 0.5  # 調整障礙物縮放比例
        self.lane_start_x = (SCREEN_WIDTH - (self.lane_width * 5)) // 2  # 水平置中

    def move_player(self, direction):
        self.player_pos[0] += direction * self.move_speed  # 調整移動速度
        # 確保人物只能在軌道範圍內移動
        self.player_pos[0] = max(self.lane_start_x, min(self.lane_start_x + self.lane_width * 5 - int(self.lane_width * self.obstacle_size), self.player_pos[0]))

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

        # 當風向和雨傘方向相反時，角色會自動移動
        if self.umbrella_direction != self.wind_direction:
            self.player_pos[0] += self.move_speed if self.wind_direction == 'RIGHT' else -self.move_speed
            self.player_pos[0] = max(self.lane_start_x, min(self.lane_start_x + self.lane_width * 5 - int(self.lane_width * self.obstacle_size), self.player_pos[0]))

        if current_time - self.last_obstacle_time > self.generate_obstacle_interval:
            # 更新障礙物數量和位置
            lane_count = random.randint(1, 5)  # 隨機決定本次生成的障礙物數量
            for _ in range(lane_count):
                lane = random.randint(0, 4)
                obstacle_image = random.choice(self.obstacle_images)
                obstacle_image = pygame.transform.scale(obstacle_image, (int(self.lane_width * self.obstacle_size), int(self.lane_width * self.obstacle_size)))
                
                # 檢查新障礙物的位置是否與現有障礙物重疊
                while any(abs(obstacle[0] - (self.lane_start_x + lane * self.lane_width + self.lane_width // 2)) < self.lane_width and abs(obstacle[1]) < int(self.lane_width * self.obstacle_size) for obstacle in self.obstacles):
                    lane = random.randint(0, 4)  # 選擇一條不同的軌道
                
                self.obstacles.append([self.lane_start_x + lane * self.lane_width + self.lane_width // 2, 0, obstacle_image])
            
            self.last_obstacle_time = current_time

        for obstacle in self.obstacles:
            obstacle[1] += 5

        self.obstacles = [ob for ob in self.obstacles if ob[1] < SCREEN_HEIGHT]

    def check_collision(self):
        for obstacle in self.obstacles:
            if abs(self.player_pos[0] - obstacle[0]) < 20 and self.player_pos[1] - obstacle[1] < 20:
                return True
        return False
