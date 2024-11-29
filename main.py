import pygame

import os, sys

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.controllers.game_controller import *

def start():

    pygame.init()
    controller = GameController()
    
    clock = pygame.time.Clock()
     
    running = True
    try:
        while running:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    controller.handle_event(event)
                elif event.type == pygame.MOUSEMOTION:
                    controller.handle_event(event)
                else:
                    continue
                    
            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print("An unexpected error occurred: %s", e)
                    
if __name__ == '__main__':
    start()
