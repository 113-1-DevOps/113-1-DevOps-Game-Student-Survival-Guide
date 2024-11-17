
import random
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Obstacle:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type = type_id  
        self.speed_multiplier = 1.0 if type_id == 0 else 1.2  

    def update_position(self, game_speed):
        """根据障碍物类型和游戏速度更新位置"""
        self.y += game_speed * self.speed_multiplier  

class OilDrum:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5  

    def update_position(self):
        """更新油桶位置"""
        self.y += self.speed

class CarAccidentModel:
    def __init__(self, level=None):
        """
        初始化 CarAccidentModel。
        如果未提供 level，将使用默认车道位置。
        """
        if level is None:
            self.lanes = [200, 300, 400, 500]
        else:
            self.lanes = level.get_lanes()
        
        self.current_lane = 1  
        self.player_x = self.lanes[self.current_lane]
        self.player_y = SCREEN_HEIGHT - 100

        if len(self.lanes) > 1:
            self.lane_width = self.lanes[1] - self.lanes[0]
        else:
            self.lane_width = 100  

        self.fuel = 100
        self.distance_to_goal = 2000  
        self.speed = 4  
        self.obstacles = []
        self.oil_drums = []
        self.school_visible = False

        self.spawn_cooldown = {lane: 0 for lane in self.lanes}  

        self.success_count = 0

        self.max_obstacles = 10
        self.max_oil_drums = 5

    def reset_for_next_level(self):
        """重置模型以进入下一个关卡"""
        self.distance_to_goal = 2000
        self.fuel = 100
        self.obstacles.clear()
        self.oil_drums.clear()
        self.speed = 4 + 0.5 * self.success_count 
        self.school_visible = False
        print(f"Reset for next level: speed={self.speed}, success_count={self.success_count}")

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
            print(f"Spawned obstacle in lane {lane} with type {type_id}")

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
            print(f"Spawned oil drum in lane {lane}")

    def update_position(self):
        """更新障碍物和油桶位置，并生成新物体"""
        for obstacle in self.obstacles[:]:
            obstacle.update_position(self.speed)
            if obstacle.y > SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
                print(f"Removed obstacle from lane {obstacle.x} as it went off screen")

        for oil_drum in self.oil_drums[:]:
            oil_drum.update_position()
            if oil_drum.y > SCREEN_HEIGHT:
                self.oil_drums.remove(oil_drum)
                print(f"Removed oil drum from lane {oil_drum.x} as it went off screen")

        obstacle_spawn_chance = 5  
        oil_drum_spawn_chance = 2   

        if random.randint(0, 100) < obstacle_spawn_chance:
            self._spawn_obstacles()
        if random.randint(0, 100) < oil_drum_spawn_chance:
            self._spawn_oil_drums()

        for lane in self.lanes:
            if self.spawn_cooldown[lane] > 0:
                self.spawn_cooldown[lane] -= 1

        self.distance_to_goal -= self.speed
        if self.distance_to_goal < 0:
            self.distance_to_goal = 0


    def move_left(self):
        """玩家向左移动到相邻车道，并减少油量"""
        if self.current_lane > 0 and self.fuel > 0:
            self.current_lane -= 1
            self.player_x = self.lanes[self.current_lane]
            self.fuel -= 1  
            if self.fuel < 0:
                self.fuel = 0
            print(f"Player moved to lane {self.current_lane}, fuel: {self.fuel}%")

    def move_right(self):
        """玩家向右移动到相邻车道，并减少油量"""
        if self.current_lane < len(self.lanes) - 1 and self.fuel > 0:
            self.current_lane += 1
            self.player_x = self.lanes[self.current_lane]
            self.fuel -= 1 
            if self.fuel < 0:
                self.fuel = 0
            print(f"Player moved to lane {self.current_lane}, fuel: {self.fuel}%")

    def check_collision(self):
        """检查玩家是否与障碍物相撞"""
        collision_threshold = 35  
        for obstacle in self.obstacles:
            if abs(self.player_x - obstacle.x) < self.lane_width // 2 and abs(self.player_y - obstacle.y) < collision_threshold:
                print(f"Collision detected with obstacle at ({obstacle.x}, {obstacle.y})")
                return True
        return False

    def check_collect_oil_drum(self):
        """检查玩家是否收集到油桶"""
        collection_threshold = 35 
        for oil_drum in self.oil_drums:
            if abs(self.player_x - oil_drum.x) < self.lane_width // 2 and abs(self.player_y - oil_drum.y) < collection_threshold:
                self.oil_drums.remove(oil_drum)
                self.refill_fuel()
                print(f"Collected oil drum at ({oil_drum.x}, {oil_drum.y}), fuel: {self.fuel}%")
                return True
        return False

    def refill_fuel(self):
        """补充油量"""
        self.fuel = min(100, self.fuel + 10)  
        print(f"Fuel refilled to {self.fuel}%")

    def reached_goal(self):
        """检查是否到达终点"""
        return self.distance_to_goal <= 0

    def increase_difficulty(self):
        """根据成功次数增加难度"""
        self.success_count += 1
        print(f"Increasing difficulty: success_count={self.success_count}")
