from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

def center_to_top_left(center_x, center_y, image_width, image_height):
    """
    根據圖片的中心座標計算並返回左上角座標。
    
    :param center_x: 圖片的中心點 x 座標
    :param center_y: 圖片的中心點 y 座標
    :param image_width: 圖片的寬度
    :param image_height: 圖片的高度
    :return: 左上角座標 (top_left_x, top_left_y)
    """
    top_left_x = center_x - image_width // 2
    top_left_y = center_y - image_height // 2
    return top_left_x, top_left_y


def scale_image(image, width_ratio, height_ratio):
    """
    根據視窗比例縮放圖片。
    
    :param image: 原始圖片 (pygame.Surface)
    :param width_ratio: 寬度相對於 SCREEN_WIDTH 的比例
    :param height_ratio: 高度相對於 SCREEN_HEIGHT 的比例
    :return: 縮放後的圖片
    """
    scaled_width = int(SCREEN_WIDTH * width_ratio)
    scaled_height = int(SCREEN_HEIGHT * height_ratio)
    return pygame.transform.scale(image, (scaled_width, scaled_height))