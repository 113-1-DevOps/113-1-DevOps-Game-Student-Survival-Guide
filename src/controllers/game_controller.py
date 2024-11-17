import pygame
from controllers.car_accident_controller import CarAccidentController
from controllers.teacherout_controller import TeacheroutController
from controllers.typhoon_controller import TyphoonController
from models.car_accident_level_model import CarAccidentModel
from models.teacherout_level_model import TeacheroutModel
from models.typhoon_level_model import TyphoonModel
from views.home_view import HomeView
from views.next_inform_view import NextInformView
from views.game_over_view import GameOverView
from models.game_model import GameModel
from config.constants import *

class GameController:
    def __init__(self):
        pygame.init()
        self.model = GameModel()
        self.view_map = {
            HOME: HomeView(),
            NEXT_INFORM: NextInformView(),
            GAME_OVER: GameOverView()
        }
        self.controller_map = {
            TYPHOON: TyphoonController(),
            TEACHEROUT: TeacheroutController(),
            CAR_ACCIDENT: CarAccidentController()
        }
        self.current_view = self.view_map[HOME]
        self.screen_state = HOME
        self.current_view.draw()
                
    def handle_event(self,event):
        if self.screen_state in self.controller_map:
            self.controller_map[self.screen_state].handle_event(event)
        else:
            event_result = self.current_view.handle_event(event)
            if event_result:
                self.process_event_result(event_result)
                self.current_view.draw()

    def process_event_result(self, event_result):
        if event_result == START or event_result == NEXT_INFORM :
            level = self.model.start_random_level()
            self.screen_state = level
            is_continue = self.controller_map[level].start()
            if(is_continue):
                self.switch_view(NEXT_INFORM)
            else:
                self.switch_view(GAME_OVER)
        elif event_result == RETRY:
            self.controller_map = {
            TYPHOON: TyphoonController(),
            TEACHEROUT: TeacheroutController(),
            CAR_ACCIDENT: CarAccidentController()
            }
            self.switch_view(HOME)

    def switch_view(self, new_state):
        self.screen_state = new_state
        self.current_view = self.view_map[self.screen_state]

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
