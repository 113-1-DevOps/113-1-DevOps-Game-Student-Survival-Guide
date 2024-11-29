# src/controllers/car_accident_controller.py

import pygame
import sys
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random

class Obstacle:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type = type_id
        self.speed_multiplier = 1.0 if type_id == 0 else 1.2

    def update_position(self, game_speed):
        self.y += game_speed * self.speed_multiplier

class OilDrum:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def update_position(self):
        self.y += self.speed

class CarAccidentModel:
    def __init__(self, level=None):
        # 初始化pygame显示，以便加载图像
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 加载背景以获取其宽度
        background = pygame.image.load("images/car_accident/car_accident_background.png").convert_alpha()
        scale_factor_bg = SCREEN_HEIGHT / background.get_height()
        background_width = int(background.get_width() * scale_factor_bg)
        background_x = (SCREEN_WIDTH - background_width) // 2

        # 定义车道在背景图片中的相对位置（根据实际背景图片调整）
        lane_positions = [0.22, 0.39, 0.59, 0.77]  # 根据实际情况调整

        # 计算每个车道的中心位置
        self.lanes = [background_x + background_width * pos for pos in lane_positions]

        self.current_lane = 1
        self.player_x = self.lanes[self.current_lane]
        self.player_y = SCREEN_HEIGHT - 100
        self.lane_width = background_width / 4  # 假设车道宽度为背景宽度的1/4

        self.fuel = 100
        self.distance_to_goal = 5000  # 增加初始距离
        self.speed = 4
        self.obstacles = []
        self.oil_drums = []
        self.school_visible = False

        self.spawn_cooldown = {lane: 0 for lane in self.lanes}

        self.success_count = 0

        self.max_obstacles = 10
        self.max_oil_drums = 5

        # 加载并缩放学校图像
        self.school_image = pygame.image.load("images/car_accident/car_accident_school.png").convert_alpha()
        # 根据需要调整学校图像的大小
        school_width = SCREEN_WIDTH // 2  # 学校的宽度为屏幕宽度的一半，您可以根据需要调整
        school_scale_factor = school_width / self.school_image.get_width()
        self.school_image = pygame.transform.scale(
            self.school_image,
            (
                school_width,
                int(self.school_image.get_height() * school_scale_factor)
            )
        )
        self.school_width = self.school_image.get_width()
        self.school_height = self.school_image.get_height()

        # 学校出现的距离
        self.school_appear_distance = 1500  # 当距离小于1500时，学校开始出现

    def reset_for_next_level(self):
        """重置模型以进入下一个关卡"""
        self.distance_to_goal = 5000
        self.fuel = 100
        self.obstacles.clear()
        self.oil_drums.clear()
        self.speed = 4 + 1 * self.success_count
        self.school_visible = False

    def _is_position_free(self, lane, y, objects, min_distance=200):
        """检查指定车道是否有足够空间避免重叠"""
        for obj in objects:
            if obj.x == lane and abs(obj.y - y) < min_distance:
                return False
        return True

    def _spawn_obstacles(self):
        """生成障碍物"""
        if len(self.obstacles) >= self.max_obstacles:
            return

        available_lanes = [lane for lane in self.lanes if self.spawn_cooldown[lane] <= 0]
        if not available_lanes:
            return

        lane = random.choice(available_lanes)
        obstacle_y = -50
        if self._is_position_free(lane, obstacle_y, self.obstacles + self.oil_drums):
            type_id = random.randint(0, 1)
            self.obstacles.append(Obstacle(lane, obstacle_y, type_id))
            self.spawn_cooldown[lane] = 90

    def _spawn_oil_drums(self):
        """生成油桶"""
        if len(self.oil_drums) >= self.max_oil_drums:
            return

        available_lanes = [lane for lane in self.lanes if self.spawn_cooldown[lane] <= 0]
        if not available_lanes:
            return

        lane = random.choice(available_lanes)
        oil_drum_y = -50
        if self._is_position_free(lane, oil_drum_y, self.obstacles + self.oil_drums):
            self.oil_drums.append(OilDrum(lane, oil_drum_y))
            self.spawn_cooldown[lane] = 90

    def update_position(self):
        """更新障碍物和油桶位置，并生成新物体"""
        # 更新障碍物位置
        for obstacle in self.obstacles[:]:
            obstacle.update_position(self.speed)
            if obstacle.y > SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)

        # 更新油桶位置
        for oil_drum in self.oil_drums[:]:
            oil_drum.update_position()
            if oil_drum.y > SCREEN_HEIGHT:
                self.oil_drums.remove(oil_drum)

        # 更新距离
        self.distance_to_goal -= self.speed
        if self.distance_to_goal < 0:
            self.distance_to_goal = 0

        # 检查学校是否可见
        if self.distance_to_goal <= self.school_appear_distance:
            self.school_visible = True
            # 计算当前学校显示的高度
            progress = (self.school_appear_distance - self.distance_to_goal) / self.school_appear_distance
            progress = max(0, min(progress, 1))  # 确保进度在0到1之间
            current_school_height = int(self.school_height * progress)
            # 移除位于学校覆盖区域内的障碍物和油桶
            self.obstacles = [ob for ob in self.obstacles if ob.y > SCREEN_HEIGHT - current_school_height]
            self.oil_drums = [od for od in self.oil_drums if od.y > SCREEN_HEIGHT - current_school_height]
        else:
            self.school_visible = False
            # 生成新的障碍物和油桶
            obstacle_spawn_chance = 5
            oil_drum_spawn_chance = 2

            if random.randint(0, 100) < obstacle_spawn_chance:
                self._spawn_obstacles()
            if random.randint(0, 100) < oil_drum_spawn_chance:
                self._spawn_oil_drums()

        # 更新生成冷却时间
        for lane in self.lanes:
            if self.spawn_cooldown[lane] > 0:
                self.spawn_cooldown[lane] -= 1

    def move_left(self):
        """玩家向左移动到相邻车道，并减少油量"""
        if self.current_lane > 0 and self.fuel > 0:
            self.current_lane -= 1
            self.player_x = self.lanes[self.current_lane]
            self.fuel -= 8
            if self.fuel < 0:
                self.fuel = 0

    def move_right(self):
        """玩家向右移动到相邻车道，并减少油量"""
        if self.current_lane < len(self.lanes) - 1 and self.fuel > 0:
            self.current_lane += 1
            self.player_x = self.lanes[self.current_lane]
            self.fuel -= 8
            if self.fuel < 0:
                self.fuel = 0

    def check_collision(self):
        """检查玩家是否与障碍物相撞"""
        collision_threshold = 35
        for obstacle in self.obstacles:
            if abs(self.player_x - obstacle.x) < self.lane_width // 2 and abs(self.player_y - obstacle.y) < collision_threshold:
                return True
        return False

    def check_collect_oil_drum(self):
        """检查玩家是否收集到油桶"""
        collection_threshold = 35
        for oil_drum in self.oil_drums:
            if abs(self.player_x - oil_drum.x) < self.lane_width // 2 and abs(self.player_y - oil_drum.y) < collection_threshold:
                self.oil_drums.remove(oil_drum)
                self.refill_fuel()
                return True
        return False

    def refill_fuel(self):
        """补充油量"""
        self.fuel = min(100,self.fuel + 10)

    def reached_goal(self):
        """检查是否到达终点"""
        return self.distance_to_goal <= 0

    def increase_difficulty(self):
        """根据成功次数增加难度"""
        self.success_count += 1
