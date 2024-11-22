# src/controllers/car_accident_controller.py

import pygame
import sys
from models.car_accident_level_model import CarAccidentModel
from views.car_accident_Levelview import CarAccidentLevelView
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class CarAccidentController:
    def __init__(self, model=None, view=None):
        """
        初始化 CarAccidentController。
        如果未提供 model 或 view，将自动创建默认实例。
        """
        if model is None:
            self.model = CarAccidentModel()
        else:
            self.model = model

        self.view = view
        self.running = True

    def start(self):
        """开始车祸关卡"""
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Display initialized with set_mode in CarAccidentController.start()")

        if self.view is None:
            self.view = CarAccidentLevelView(self.model)
            print("CarAccidentLevelView initialized in CarAccidentController.start()")

        self.running = True
        clock = pygame.time.Clock()
        level_result = False  

        print(f"Starting level with speed: {self.model.speed} and success_count: {self.model.success_count}")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.model.move_left()
                        print("Player moved left")
                    elif event.key == pygame.K_RIGHT:
                        self.model.move_right()
                        print("Player moved right")

            self.model.update_position()

            print(f"Current speed: {self.model.speed}")

            if self.model.check_collision() or self.model.fuel <= 0:
                self.running = False
                level_result = False  
                print("Level failed: Collision or fuel depleted")
            elif self.model.reached_goal():
                self.model.increase_difficulty()
                self.model.reset_for_next_level()
                self.running = False
                level_result = True  
                print("Level succeeded: Reached goal")

            if self.model.check_collect_oil_drum():
                self.model.refill_fuel()
                print("Collected oil drum: Fuel refilled")

            self.view.draw()

            clock.tick(60)

        print(f"Ending level with speed: {self.model.speed} and success_count: {self.model.success_count}")

        return level_result
