# game_model.py
import random

from config.constants import *

class LevelModel:
    def __init__(self, level_name):
        self.level_name = level_name
        self.is_completed = False

    def update(self):
        # 模擬更新邏輯
        pass

class GameModel:
    def __init__(self):
        self.levels = [TEACHEROUT]
        self.current_level = None

    def start_random_level(self):
        self.current_level = random.choice(self.levels)
        return self.current_level
