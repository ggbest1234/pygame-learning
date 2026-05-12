import pygame
import sys

# 初始化 Pygame
pygame.init()

# 创建窗口 (800x600)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("我的第一个 Pygame 窗口 🎮")

# 设置颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 按 ESC 退出
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 填充黑色背景
    screen.fill(BLACK)
    
    # 在屏幕中央画一个绿色方块
    pygame.draw.rect(screen, GREEN, (375, 275, 50, 50))
    
    # 画一个红色圆形
    pygame.draw.circle(screen, RED, (400, 150), 30)
    
    # 更新显示
    pygame.display.flip()

# 退出
pygame.quit()
sys.exit()
