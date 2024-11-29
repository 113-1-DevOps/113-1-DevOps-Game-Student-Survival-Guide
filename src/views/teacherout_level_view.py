# src/views/teacherout_level_view.py
import pygame
from config.constants import *
from views.game_over_view import GameOverView
from views.next_inform_view import NextInformView

def show_failure_screen():
    """
    顯示遊戲失敗畫面
    """
    # screen = pygame.display.get_surface()
    # font = pygame.font.SysFont(None, 55)
    # text = font.render("遊戲失敗！", True, (255, 0, 0))
    # screen.blit(text, (300, 250))
    # pygame.display.update()

    pygame.init()  # 確保 Pygame 已初始化
    game_over_view = GameOverView()
    # game_over_view.draw()

def show_success_screen():
    """
    顯示遊戲成功畫面
    """
    # screen = pygame.display.get_surface()
    # font = pygame.font.SysFont(None, 55)
    # text = font.render("恭喜！成功完成任務！", True, (0, 255, 0))
    # screen.blit(text, (150, 250))
    # pygame.display.update()
    pygame.init()
    next_inform_view = NextInformView()

def update_teacher_image(screen, image_path):
    """
    更新老師的圖片
    """
    try:
        teacher_image = pygame.image.load(image_path)
        teacher_image = pygame.transform.scale(teacher_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 確保圖片適配螢幕大小
        screen.blit(teacher_image, (0, 0))  # 繪製圖片到螢幕
        pygame.display.update()  # 更新螢幕
    except pygame.error as e:
        print(f"Error updating teacher image: {e}")
