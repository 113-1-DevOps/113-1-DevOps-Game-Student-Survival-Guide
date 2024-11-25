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

        if self.view is None:
            self.view = CarAccidentLevelView(self.model)    

        if self.view is None:
            self.view = CarAccidentLevelView(self.model)

        self.running = True
        clock = pygame.time.Clock()
        level_result = False  


        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.model.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.model.move_right()

            self.model.update_position()

            if self.model.check_collision() or self.model.fuel <= 0:
                self.running = False
                level_result = False  
            elif self.model.reached_goal():
                self.model.increase_difficulty()
                self.model.reset_for_next_level()
                self.running = False
                level_result = True  
            
            if self.model.check_collect_oil_drum():
                self.model.refill_fuel()

            if self.model.check_collect_oil_drum():
                self.model.refill_fuel()

            self.view.draw()

            clock.tick(60)

        return level_result
    # 測試「車禍」關卡
    # def process_event_result(self, event_result):
    #     if event_result == START or event_result == NEXT_INFORM:
    #         level = CAR_ACCIDENT  
    #         self.screen_state = level
    #         is_continue = self.controller_map[level].start()
    #         if is_continue:
    #             self.switch_view(NEXT_INFORM)
    #         else:
    #             self.switch_view(GAME_OVER)
    #     elif event_result == RETRY:
    #         self.controller_map = {
    #             TYPHOON: TyphoonController(),
    #             TEACHEROUT: TeacheroutController(),
    #             CAR_ACCIDENT: CarAccidentController()
    #         }
    #         self.switch_view(HOME)
