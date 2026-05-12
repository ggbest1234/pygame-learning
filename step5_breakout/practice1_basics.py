"""
练习 1: 打砖块基础框架
填写代码中的 ____ 部分
"""
import pygame
import math

pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("练习 1: 打砖块 - 基础框架")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# 挡板设置
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_Y = 550  # 挡板在屏幕底部的位置
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

# 小球设置
BALL_SIZE = 12
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 4
ball_speed_y = -4  # 向上飞

# 游戏状态
game_over = False

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    # 1. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # TODO 1: 按 R 键重新开始
        # 填写代码: 如果按下 R 键且游戏结束，重置球的位置和速度
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                ball_x = SCREEN_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2
                ball_speed_x = 4
                ball_speed_y = -4
                game_over = False
    
    # 2. 更新游戏状态
    if not game_over:
        # TODO 2: 用键盘控制挡板
        keys = pygame.key.get_pressed()
        # 填写代码: 如果按左方向键，挡板左移（每次 8 像素）
        # 提示: paddle_x -= 8
        if keys[pygame.K_LEFT]:
            paddle_x -= 8
        if keys[pygame.K_RIGHT]:
            paddle_x += 8
        
        # TODO 3: 挡板不能移出屏幕
        # 填写代码: 确保 paddle_x 在 0 到 SCREEN_WIDTH - PADDLE_WIDTH 之间
        paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))
        
        # 小球移动
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        
        # TODO 4: 小球碰撞左右边界
        # 填写代码: 如果小球碰到左边界或右边界，水平速度反弹
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        
        # 小球碰撞上边界
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y
        
        # 小球落到底部 = 游戏结束
        if ball_y >= SCREEN_HEIGHT:
            game_over = True
        
        # 挡板碰撞检测
        paddle_rect = pygame.Rect(paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(ball_x - BALL_SIZE//2, ball_y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        
        # TODO 5: 小球碰撞挡板
        # 填写代码: 如果小球碰到挡板，垂直速度反弹
        if ball_rect.colliderect(paddle_rect):
            ball_speed_y = -ball_speed_y
    
    # 3. 绘制
    screen.fill(BLACK)
    
    # 绘制挡板
    pygame.draw.rect(screen, BLUE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # 绘制小球
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE // 2)
    
    # TODO 6: 显示游戏结束提示
    # 填写代码: 如果 game_over 为 True，显示 "游戏结束" 和 "按 R 重新开始"
    if game_over == True:
        font = pygame.font.SysFont("arial", 48)
        text = font.render("游戏结束，按R重新开始！", True, RED)
        screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
