# import pygame
# from views.ViewManager import MainScreenView, InstructionScreenView

# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("學生生存手冊")

# # 初始化主畫面
# main_screen_view = MainScreenView(screen)
# instruction_screen_view = None  # 初始時設為 None
# current_view = "main"  # 用來追蹤當前畫面

# running = True
# while running:
#     screen.fill((0, 0, 0))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if current_view == "main" and main_screen_view.button_rect.collidepoint(event.pos):
#                 # 切換到說明頁
#                 instruction_screen_view = InstructionScreenView(screen)
#                 current_view = "instruction"

#     # 根據當前畫面進行渲染
#     if current_view == "main":
#         main_screen_view.render()
#     elif current_view == "instruction":
#         instruction_screen_view.render()

#     pygame.display.flip()

# pygame.quit()
