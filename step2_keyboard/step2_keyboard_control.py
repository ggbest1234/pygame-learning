"""
Step 2: 键盘控制与移动
学习目标:
1. 使用键盘控制角色移动
2. 边界限制
3. 简单的碰撞检测
"""
import pygame

pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Step 2: 键盘控制")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# 玩家设置
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT // 2 - player_size // 2
player_speed = 5

# 收集物品设置
coin_size = 30
coin_x = 200
coin_y = 200
coin_collected = False

# 分数
score = 0

# 字体
try:
    font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
except:
    font = pygame.font.SysFont("arial", 24)

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    # 1. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. 更新游戏状态
    
    # 获取键盘状态
    keys = pygame.key.get_pressed()
    
    # 方向键控制移动
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # 边界限制 - 确保角色不会移出屏幕
    player_x = max(0, min(player_x, SCREEN_WIDTH - player_size))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - player_size))
    
    # 碰撞检测（玩家与金币）
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
    
    if player_rect.colliderect(coin_rect) and not coin_collected:
        coin_collected = True
        score += 10
        # 重新生成金币位置
        import random
        coin_x = random.randint(50, SCREEN_WIDTH - 50)
        coin_y = random.randint(50, SCREEN_HEIGHT - 50)
        coin_collected = False
    
    # 3. 绘制
    screen.fill(BLACK)
    
    # 绘制玩家（绿色方块）
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
    
    # 绘制金币（黄色圆形）
    pygame.draw.circle(screen, YELLOW, (coin_x + coin_size//2, coin_y + coin_size//2), coin_size//2)
    
    # 显示分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 显示操作说明
    hint_text = font.render("使用方向键 ← → ↑ ↓ 移动", True, (200, 200, 200))
    screen.blit(hint_text, (10, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
