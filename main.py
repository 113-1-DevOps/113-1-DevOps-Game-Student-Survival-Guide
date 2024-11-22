import pygame
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.controllers.game_controller import *

def start():
    pygame.init()
    controller = GameController()
    # screen_state = HOME
    # controller.draw(HOME)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                controller.handle_event(event)
        
            
if __name__=='__main__':
    start()
