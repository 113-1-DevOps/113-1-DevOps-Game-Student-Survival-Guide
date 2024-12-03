import pygame
import random
import time
from config.constants import *
from src.models.teacherout_level_model import TeacheroutModel

class TeacheroutController:
    def __init__(self):
        pygame.init()
        self.model = TeacheroutModel()
        self.time_limit = 60
        self.clicks = 0
        self.is_task_visible = False  # 按鈕是否顯示
        self.level = 1  # 初始關卡數

        # 定義所有可能的任務
        self.tasks = [
            {
                "name": "吃飯糰",
                "turned_image_path": "images/hide_from_teacher/hide_from_teacher_eating.png",
                "button_image_path": "images/hide_from_teacher/hide_from_teacher_button_eating.png",
                "button_position": (SCREEN_WIDTH - 265, 140),
            },
            {
                "name": "滑手機",
                "turned_image_path": "images/hide_from_teacher/hide_from_teacher_playing.png",
                "button_image_path": "images/hide_from_teacher/hide_from_teacher_button_playing.png",
                "button_position": (SCREEN_WIDTH - 265, 140),
            },
        ]

        # 預設圖片（老師面對學生）
        self.default_image_path = "images/hide_from_teacher/hide_from_teacher_not_moving.png"

        # 當前任務
        self.current_task = None

    def start(self) -> bool:
        print(f'關卡 {self.level} 開始')
        return self.play_level()

    def play_level(self) -> bool:
        start_time = time.time()
        time_left = self.time_limit
        game_in_progress = True
        self.clicks = 0  # 重置點擊次數

        # 隨機選擇任務
        self.current_task = random.choice(self.tasks)
        print(f"本次任務：{self.current_task['name']}")

        # 初始化畫面
        screen = self.initialize_screen(self.default_image_path)
        if screen is None:
            print("初始化螢幕失敗，遊戲結束。")
            return False

        # pygame.time.wait(500)

        next_turn_time = start_time + 3
        is_teacher_turned = False  # 老師是否背對

        while game_in_progress and time_left > 0:
            current_time = time.time()
            time_left = self.time_limit - (current_time - start_time)

            # 檢查遊戲成功條件
            if self.clicks >= self.model.success_clicks:
                self.show_success_screen()
                self.level += 1  # 關卡加一
                self.model.success_clicks += 5  # 提高過關點擊數
                print(f"恭喜過關！已提升至關卡 {self.level}")
                return True

            # 處理滑鼠點擊事件
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    button_rect = pygame.Rect(*self.current_task["button_position"], 100, 100)

                    if not self.is_task_visible:
                        print("非法點擊！遊戲結束。")
                        self.show_failure_screen()
                        return False
                    elif button_rect.collidepoint(mouse_x, mouse_y):
                        self.clicks += 1
                        # print(f"點擊次數: {self.clicks}")

            # 檢查時間是否用完
            if time_left <= 0:
                self.show_failure_screen()
                return False

            # 老師回頭與面對學生的邏輯
            if current_time >= next_turn_time:
                if is_teacher_turned:  # 老師背對 -> 準備面對學生
                    self.flash_red_light(screen)  # 閃紅光提醒
                    self.update_teacher_image(screen, self.default_image_path)  # 老師轉回面對學生
                    self.is_task_visible = False  # 確保按鈕隱藏
                    is_teacher_turned = False  # 更新老師狀態
                else:  # 老師面對學生 -> 背對
                    self.update_teacher_image(screen, self.current_task["turned_image_path"])  # 老師背對
                    self.show_task_button(screen)  # 顯示當前任務的按鈕
                    is_teacher_turned = True  # 更新老師狀態

                next_turn_time = current_time + 3  # 設定下一次轉頭的時間

            self.draw_click_info(screen, time_left)  # 繪製點擊資訊
            pygame.display.update()
            time.sleep(0.1)

        self.show_failure_screen()
        return False

    def initialize_screen(self, image_path):
        try:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            # pygame.display.set_caption("Teacher Out Game")  # 設定視窗標題

            teacher_image = pygame.image.load(image_path)
            teacher_image = pygame.transform.scale(teacher_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(teacher_image, (0, 0))
            pygame.display.update()
            return screen
        except FileNotFoundError:
            print(f"圖片檔案未找到：{image_path}")
            return None
        except pygame.error as e:
            print(f"Error initializing screen: {e}")
            return None

    def show_task_button(self, screen):
        button_image = pygame.image.load(self.current_task["button_image_path"])
        button_image = pygame.transform.scale(button_image, (100, 100))
        screen.blit(button_image, self.current_task["button_position"])
        self.is_task_visible = True

    def update_teacher_image(self, screen, image_path):
        teacher_image = pygame.image.load(image_path)
        teacher_image = pygame.transform.scale(teacher_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(teacher_image, (0, 0))

    def flash_red_light(self, screen):
        red_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        red_surface.fill((255, 0, 0))
        red_surface.set_alpha(100)
        screen.blit(red_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)

    def show_success_screen(self):
        print("恭喜你，遊戲成功！")
        pygame.time.wait(2000)

    def show_failure_screen(self):
        print("很可惜，遊戲失敗！")
        pygame.time.wait(2000)

    def draw_click_info(self, screen, time_left):
        # 獲取背景圖的表面
        background_surface = pygame.image.load(self.default_image_path)
        background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 從背景圖中提取顏色
        average_color = pygame.transform.average_color(background_surface, pygame.Rect(0, 0, 200, 50))
        
        # 填充背景顏色
        info_background_rect = pygame.Rect(0, 0, 200, 50)
        pygame.draw.rect(screen, average_color, info_background_rect)
        
        # 繪製文字
        font = pygame.font.Font(None, 24)
        time_text = font.render(f"Time Left: {int(time_left)}s", True, (255, 255, 255))  # 剩餘時間
        click_text = font.render(f"Click Count: {self.clicks}", True, (255, 255, 255))  # 點擊次數
        goal_text = font.render(f"Goal Count: {self.model.success_clicks}", True, (255, 255, 255))  # 目標次數
        screen.blit(time_text, (10, 10))  
        screen.blit(click_text, (10, 30))
        screen.blit(goal_text, (10, 50))
