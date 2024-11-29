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
        self.levels = [TYPHOON,TEACHEROUT,CAR_ACCIDENT]
        self.current_level = None
        self.test_mode = False  # 設置測試模式開關

    def start_random_level(self):
        # self.current_level = random.choice(self.levels)
        # return self.current_level
        if self.test_mode:
            # 方便測試固定關卡用(可刪)
            self.current_level = TYPHOON
        else:
            # 隨機選擇關卡
            self.current_level = random.choice(self.levels)
        return self.current_level
