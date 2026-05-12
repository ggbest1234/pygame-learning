"""
练习 3: 砖块数组与碰撞检测
创建多行多列的砖块，并实现小球与砖块的碰撞检测
"""
import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("练习 3: 砖块数组")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

# 挡板
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_Y = 550
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

# 小球
BALL_SIZE = 12
ball_x = SCREEN_WIDTH // 2
ball_y = 400
ball_speed_x = 3
ball_speed_y = -4

# 游戏状态
score = 0
lives = 3
font = pygame.font.SysFont("arial", 24)

# TODO 1: 创建砖块数组
# 砖块设置
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = 80
BRICK_HEIGHT = 25
BRICK_GAP = 5
BRICK_START_Y = 50

# 创建砖块列表
# 提示: 使用列表推导式创建二维数组
# bricks = [[... for col in range(BRICK_COLS)] for row in range(BRICK_ROWS)]
# 每个砖块应该是一个字典，包含: rect, color, active
bricks = []

# 不同行的颜色
colors = [RED, ORANGE, YELLOW, GREEN, CYAN]

def create_bricks():
    """初始化所有砖块"""
    global bricks
    bricks = []
    for row in range(BRICK_ROWS):
        row_bricks = []
        for col in range(BRICK_COLS):
            # TODO 2: 计算每个砖块的位置
            # x = 起始x + 列号 * (砖块宽度 + 间隙)
            # y = 起始y + 行号 * (砖块高度 + 间隙)
            brick_x = (col) * (BRICK_WIDTH +BRICK_GAP)
            brick_y = BRICK_START_Y+(row) * (BRICK_HEIGHT + BRICK_GAP)
            
            # 创建砖块字典
            brick = {
                "ROW_DATA":row,
                "rect": pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT),
                "color": colors[row],  # 每行不同颜色
                "active": True
            }
            row_bricks.append(brick)
        bricks.append(row_bricks)

def reset_ball():
    """重置小球"""
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = 3
    ball_speed_y = -4

# 初始化砖块
create_bricks()

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # 重新开始
                lives = 3
                score = 0
                reset_ball()
                create_bricks()
    
    # 更新
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 8
    if keys[pygame.K_RIGHT]:
        paddle_x += 8
    
    paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))
    
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # 碰撞左右边界
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x
    
    # 碰撞上边界
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    
    # 碰撞挡板
    paddle_rect = pygame.Rect(paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x - BALL_SIZE//2, ball_y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    
    if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
        ball_speed_y = -ball_speed_y
    
    # TODO 3: 检测小球与砖块的碰撞
    # 提示: 遍历所有砖块，检查 active 和碰撞
    for row in bricks:
        for brick in row:
            if brick["active"] and ball_rect.colliderect(brick["rect"]):
                brick["active"] = False
                ball_speed_y = - ball_speed_y
                score += (5-brick["ROW_DATA"])*10 # 不同行不同分数
                break
    
    # 小球掉落
    if ball_y >= SCREEN_HEIGHT:
        lives -= 1
        if lives > 0:
            reset_ball()
        else:
            # 游戏结束，停止球
            ball_speed_x = 0
            ball_speed_y = 0
    
    # 绘制
    screen.fill(BLACK)
    
    # 绘制砖块
    for row in bricks:
        for brick in row:
            if brick["active"]:
                pygame.draw.rect(screen, brick["color"], brick["rect"])
                pygame.draw.rect(screen, WHITE, brick["rect"], 1)  # 边框
    
    # 绘制挡板
    pygame.draw.rect(screen, BLUE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # 绘制小球
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE // 2)
    
    # 显示分数和生命
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    lives_text = font.render(f"生命: {lives}", True, RED)
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    
    # 游戏结束提示
    if lives <= 0:
        over_font = pygame.font.SysFont("arial", 48)
        over_text = over_font.render("GAME OVER", True, RED)
        screen.blit(over_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 50))
        
        restart_text = font.render("按 R 重新开始", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
