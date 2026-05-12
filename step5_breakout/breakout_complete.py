"""
Step 5: 打砖块完整版 (Breakout)
综合应用：球物理、角度反射、砖块数组、生命系统
"""
import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打砖块 - Breakout")

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
PINK = (255, 100, 150)

# 游戏状态
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_WIN = 3

current_state = STATE_MENU

# 字体
try:
    font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    big_font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 48)
except:
    font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 48)

# 挡板设置
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_Y = 550
PADDLE_SPEED = 10
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

# 小球设置
BALL_SIZE = 12
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 4
ball_speed_y = -4
BALL_BASE_SPEED = 5

# 游戏数据
score = 0
lives = 3
high_score = 0

# 砖块设置
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_GAP_X = 5
BRICK_GAP_Y = 5
BRICK_START_Y = 60

# 每行颜色和分值
ROW_DATA = [
    {"color": RED, "points": 50},
    {"color": ORANGE, "points": 40},
    {"color": YELLOW, "points": 30},
    {"color": GREEN, "points": 20},
    {"color": CYAN, "points": 10}
]

# 砖块列表 (二维数组: [row][col])
bricks = []

def create_bricks():
    """创建砖块数组"""
    global bricks
    bricks = []
    
    # 计算起始X坐标（居中）
    total_width = BRICK_COLS * BRICK_WIDTH + (BRICK_COLS - 1) * BRICK_GAP_X
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    for row in range(BRICK_ROWS):
        row_bricks = []
        for col in range(BRICK_COLS):
            brick_x = start_x + col * (BRICK_WIDTH + BRICK_GAP_X)
            brick_y = BRICK_START_Y + row * (BRICK_HEIGHT + BRICK_GAP_Y)
            
            brick = {
                "rect": pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT),
                "color": ROW_DATA[row]["color"],
                "points": ROW_DATA[row]["points"],
                "active": True
            }
            row_bricks.append(brick)
        bricks.append(row_bricks)

def reset_ball():
    """重置小球到中间，随机水平速度"""
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    # 随机水平速度（-3 到 3）
    ball_speed_x = (pygame.time.get_ticks() % 7) - 3
    ball_speed_y = -BALL_BASE_SPEED

def reset_game():
    """重置整个游戏"""
    global score, lives, current_state, paddle_x
    score = 0
    lives = 3
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    create_bricks()
    reset_ball()

def check_win():
    """检查是否所有砖块都被打碎"""
    for row in bricks:
        for brick in row:
            if brick["active"]:
                return False
    return True

def handle_paddle_bounce():
    """处理挡板碰撞和角度反射"""
    global ball_speed_x, ball_speed_y
    
    paddle_center = paddle_x + PADDLE_WIDTH / 2
    hit_pos = (ball_x - paddle_center) / (PADDLE_WIDTH / 2)  # -1.0 到 1.0
    
    # 最大反弹角度 60度 (1.047 弥度)
    max_angle = math.radians(60)
    angle = hit_pos * max_angle
    
    # 计算新速度
    speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
    ball_speed_x = speed * math.sin(angle)
    ball_speed_y = -abs(speed * math.cos(angle))  # 确保向上弹

def update_game():
    """更新游戏逻辑"""
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, lives, current_state,paddle_x
    
    # 挡板移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        paddle_x += PADDLE_SPEED
    
    # 挡板边界限制
    paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))
    
    # 小球移动
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    ball_rect = pygame.Rect(ball_x - BALL_SIZE//2, ball_y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    
    # 碰撞左右边界
    if ball_x <= BALL_SIZE//2 or ball_x >= SCREEN_WIDTH - BALL_SIZE//2:
        ball_speed_x = -ball_speed_x
    
    # 碰撞上边界
    if ball_y <= BALL_SIZE//2:
        ball_speed_y = -ball_speed_y
    
    # 碰撞挡板
    paddle_rect = pygame.Rect(paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
        handle_paddle_bounce()
        ball_y = PADDLE_Y - BALL_SIZE//2 - 1  # 防止粘连
    
    # 碰撞砖块
    for row in bricks:
        for brick in row:
            if brick["active"] and ball_rect.colliderect(brick["rect"]):
                brick["active"] = False
                score += brick["points"]
                ball_speed_y = -ball_speed_y
                break
    
    # 检查是否胜利
    if check_win():
        current_state = STATE_WIN
        return
    
    # 小球掉落
    if ball_y >= SCREEN_HEIGHT:
        lives -= 1
        if lives > 0:
            reset_ball()
        else:
            current_state = STATE_GAME_OVER

def draw_gradient_background():
    """绘制渐变背景"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(10 + 20 * ratio)
        g = int(10 + 30 * ratio)
        b = int(30 + 40 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def draw_game():
    """绘制游戏画面"""
    draw_gradient_background()
    
    # 绘制砖块
    for row in bricks:
        for brick in row:
            if brick["active"]:
                pygame.draw.rect(screen, brick["color"], brick["rect"])
                pygame.draw.rect(screen, WHITE, brick["rect"], 2)
    
    # 绘制挡板
    pygame.draw.rect(screen, BLUE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT), 2)
    
    # 绘制小球
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE // 2)
    pygame.draw.circle(screen, (200, 200, 200), (int(ball_x), int(ball_y)), BALL_SIZE // 2 - 2)
    
    # 绘制UI
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    lives_text = font.render(f"生命: {lives}", True, RED)
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

def draw_menu():
    """绘制开始菜单"""
    draw_gradient_background()
    
    title = big_font.render("打砖块", True, YELLOW)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(title, title_rect)
    
    subtitle = font.render("使用左右方向键移动挡板", True, WHITE)
    sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(subtitle, sub_rect)
    
    start_text = font.render("按空格键开始游戏", True, GREEN)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(start_text, start_rect)

def draw_game_over():
    """绘制游戏结束画面"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    over_text = big_font.render("游戏结束", True, RED)
    over_rect = over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(over_text, over_rect)
    
    score_text = font.render(f"最终分数: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
    screen.blit(score_text, score_rect)
    
    restart_text = font.render("按 R 重新开始", True, YELLOW)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
    screen.blit(restart_text, restart_rect)

def draw_win():
    """绘制胜利画面"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    win_text = big_font.render("恭喜胜利！", True, GREEN)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(win_text, win_rect)
    
    score_text = font.render(f"最终分数: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
    screen.blit(score_text, score_rect)
    
    restart_text = font.render("按 R 重新开始", True, YELLOW)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
    screen.blit(restart_text, restart_rect)

# 初始化
create_bricks()

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_state == STATE_MENU:
                current_state = STATE_PLAYING
            
            if event.key == pygame.K_r and current_state in (STATE_GAME_OVER, STATE_WIN):
                reset_game()
                current_state = STATE_MENU
    
    # 更新
    if current_state == STATE_PLAYING:
        update_game()
    
    # 绘制
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_PLAYING:
        draw_game()
    elif current_state == STATE_GAME_OVER:
        draw_game()
        draw_game_over()
    elif current_state == STATE_WIN:
        draw_game()
        draw_win()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
