"""
Pygame Step 3 - 时间动画练习
============================
学习目标: 用 sin/cos 制作闪烁和摇摆效果

核心公式:
    value = math.sin(pygame.time.get_ticks() / 周期)
    闪烁亮度 = abs(math.sin(time / 500))  # 0.0 ~ 1.0
"""

import pygame
import math

# ========== 初始化 ==========
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("时间动画练习 - 闪烁金币与摇摆敌人")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# ========== 渐变背景 ==========
def draw_gradient(screen):
    """绘制深蓝到浅蓝的渐变"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(0 + (100 - 0) * ratio)
        g = int(0 + (150 - 0) * ratio)
        b = int(100 + (255 - 100) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

# ========== 游戏循环 ==========
running = True
score = 0

while running:
    # 1. 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # ========== 在这里填空 - 时间动画 ==========
    
    # 获取游戏已运行的毫秒数
    time_ms = pygame.time.get_ticks()
    
    # 练习1: 闪烁的金币
    # 目标: 金币颜色在 (255, 200, 0) 和 (255, 100, 0) 之间变化
    # 提示: 亮度 = abs(sin(time / 500))
    
    # ========== 在这里填空 ==========
    brightness = abs(math.sin(time_ms/500))  # 亮度在 0.0 ~ 1.0 之间变化
    coin_g = int(200 - 100 * brightness)  # 绿色从 200变到100
    coin_color = (255, coin_g, 0)
    # ================================
    
    # 练习2: 左右摇摆的敌人
    # 目标: 敌人在屏幕中心 (400, 300) 左右 150 像素范围内摇摆
    # 提示: enemy_x = 400 + sin(time / 1000) * 150
    
    # ========== 在这里填空 ==========
    enemy_x = 400 + math.sin(time_ms/1000)*150
    enemy_y = 300
    # ================================
    
    # 练习3（挑战）: 呼吸效果的玩家
    # 目标: 玩家大小在 1.0 到 1.3 之间变化，周期约 800ms
    # 提示: scale = 1.0 + 0.15 * sin(time / 800)
    
    player_scale = 1.0  # 默认不变化
    # 取消下面注释来完成练习3
    player_scale = 1.0 + 0.15*math.sin(time_ms/800)
    
    player_size = int(40 * player_scale)
    player_x = 200
    player_y = 400
    
    # ========== 绘制 ==========
    # 绘制渐变背景
    draw_gradient(screen)
    
    # 绘制闪烁的金币
    pygame.draw.circle(screen, coin_color, (600, 200), 30)
    pygame.draw.circle(screen, (255, 255, 200), (590, 190), 8)  # 高光
    
    # 显示金币标签
    coin_label = font.render("COIN", True, (255, 255, 255))
    screen.blit(coin_label, (580, 240))
    
    # 绘制摇摆的敌人
    pygame.draw.rect(screen, (255, 80, 80), (enemy_x - 25, enemy_y - 25, 50, 50))
    pygame.draw.rect(screen, (200, 50, 50), (enemy_x - 15, enemy_y - 10, 10, 10))  # 眼睛
    pygame.draw.rect(screen, (200, 50, 50), (enemy_x + 5, enemy_y - 10, 10, 10))   # 眼睛
    
    # 显示敌人标签
    enemy_label = font.render("ENEMY", True, (255, 255, 255))
    screen.blit(enemy_label, (enemy_x - 35, enemy_y + 35))
    
    # 绘制呼吸的玩家
    pygame.draw.rect(screen, (80, 200, 80), 
                     (player_x - player_size//2, player_y - player_size//2, 
                      player_size, player_size))
    
    # 显示玩家标签
    player_label = font.render("PLAYER", True, (255, 255, 255))
    screen.blit(player_label, (player_x - 35, player_y + player_size//2 + 10))
    
    # 显示说明
    instructions = [
        "练习1: 填充 brightness 使金币闪烁",
        "练习2: 填充 enemy_x 使敌人左右摇摆", 
        "练习3(挑战): 填充 player_scale 使玩家呼吸",
        "",
        "按 ESC 退出"
    ]
    for i, text in enumerate(instructions):
        surface = font.render(text, True, (255, 255, 255))
        screen.blit(surface, (10, 10 + i * 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
