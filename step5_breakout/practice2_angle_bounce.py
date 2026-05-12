"""
练习 2: 挡板角度反射
核心概念: 小球击中挡板的位置决定反弹角度
"""
import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("练习 2: 挡板角度反射")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# 挡板
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_Y = 550
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

# 小球
BALL_SIZE = 12
ball_x = SCREEN_WIDTH // 2
ball_y = 400
ball_speed_x = 0
ball_speed_y = 5  # 初始垂直向下运动

# 游戏状态
score = 0
font = pygame.font.SysFont("arial", 24)

def reset_ball():
    """重置小球到中间，并向随机方向发射"""
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    # 随机水平速度（-4 到 4），垂直向上
    ball_speed_x = (pygame.time.get_ticks() % 9) - 4
    ball_speed_y = -5

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_ball()
    
    # 更新
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 10
    if keys[pygame.K_RIGHT]:
        paddle_x += 10
    
    # 挡板边界限制
    paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))
    
    # 小球移动
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # 碰撞左右边界
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x
    
    # 碰撞上边界
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    
    # 挡板碰撞检测
    paddle_rect = pygame.Rect(paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x - BALL_SIZE//2, ball_y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    
    if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
        """
        TODO: 实现角度反射
        
        核心逻辑:
        1. 计算小球击中挡板的位置（-1 到 1）
           -1 = 击中左边缘, 0 = 击中中心, 1 = 击中右边缘
        
        2. 根据击中位置计算反弹角度（弥度）
        
        3. 设置新的速度矢量
        """
        # 计算击中位置 (-1 到 1)
        # 提示: (ball_x - paddle_center) / (paddle_width / 2)
        paddle_center = paddle_x + PADDLE_WIDTH / 2
        hit_pos = (ball_x - paddle_center) / (PADDLE_WIDTH / 2)  # 填写这行
        
        # 最大反弹角度（弥度）60度 = 1.047 弥度
        angle = hit_pos * math.radians(60) # 填写最大角度
        
        # 计算新速度 (速度大小保持 5)
        ball_speed_x = 5 * math.sin(angle)
        ball_speed_y = -5 * math.cos(angle)
        
        score += 10
    
    # 小球落到底部
    if ball_y >= SCREEN_HEIGHT:
        ball_speed_y = 0
        ball_speed_x = 0
    
    # 绘制
    screen.fill(BLACK)
    
    # 绘制挡板
    pygame.draw.rect(screen, BLUE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # 绘制小球
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE // 2)
    
    # 绘制击中点标记（帮助理解）
    paddle_center = paddle_x + PADDLE_WIDTH / 2
    pygame.draw.line(screen, GREEN, (paddle_center, PADDLE_Y), (paddle_center, PADDLE_Y + PADDLE_HEIGHT), 2)
    
    # 显示分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 显示说明
    hint_text = font.render("左右方向键移动 | 空格键重新发球", True, YELLOW)
    screen.blit(hint_text, (10, SCREEN_HEIGHT - 30))
    
    # 显示角度反射说明
    if ball_speed_y > 0:
        bounce_text = font.render("球下落中... 准备接球！", True, RED)
    else:
        bounce_text = font.render("球反弹中...", True, GREEN)
    screen.blit(bounce_text, (SCREEN_WIDTH - 200, 10))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
