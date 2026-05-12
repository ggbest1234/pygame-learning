import pygame
import sys
import os
import time
import math

# ========== 初始化 ==========
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)  # 初始化音频：44.1kHz, 16位, 单声道

# 设置窗口
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("第3课：图片、角色与音效 🎨🎵")

# 创建时钟对象
clock = pygame.time.Clock()
FPS = 60

# ========== 资源路径 ==========
ASSETS_DIR = os.path.expanduser("~/pygame_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ========== 创建玩家图片 ==========
PLAYER_IMG_PATH = os.path.join(ASSETS_DIR, "player.png")
if not os.path.exists(PLAYER_IMG_PATH):
    # 创建一个50x50的绿色圆形
    temp_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(temp_surface, (50, 200, 50), (25, 25), 25)
    pygame.draw.circle(temp_surface, (30, 150, 30), (25, 25), 20)
    # 画眼睛
    pygame.draw.circle(temp_surface, (255, 255, 255), (17, 20), 6)
    pygame.draw.circle(temp_surface, (255, 255, 255), (33, 20), 6)
    pygame.draw.circle(temp_surface, (0, 0, 0), (17, 20), 3)
    pygame.draw.circle(temp_surface, (0, 0, 0), (33, 20), 3)
    pygame.image.save(temp_surface, PLAYER_IMG_PATH)
    print(f"✓ 创建了玩家图片: {PLAYER_IMG_PATH}")

# ========== 加载图片 ==========
try:
    player_img = pygame.image.load(PLAYER_IMG_PATH)
    player_img = pygame.transform.scale(player_img, (50, 50))
    print("✓ 图片加载成功！")
except pygame.error as e:
    print(f"✗ 图片加载失败: {e}")
    player_img = None

# ========== 创建音效 ==========
def create_beep_sound(frequency=440, duration_ms=100, volume=0.3):
    """用Pygame自带功能创建简单的噗声（不依赖numpy）"""
    sample_rate = 44100
    samples = int(sample_rate * duration_ms / 1000)
    
    # 创建音频buffer
    import array
    buf = array.array('h')  # 有符号短整数
    
    max_val = int(32767 * volume)
    for i in range(samples):
        # 生成正弦波
        import math
        t = i / sample_rate
        val = int(max_val * math.sin(2 * math.pi * frequency * t))
        buf.append(val)
    
    return pygame.mixer.Sound(buffer=buf)

# 创建移动音和收集音
try:
    move_sound = create_beep_sound(frequency=300, duration_ms=50, volume=0.2)   # 低音噗
    collect_sound = create_beep_sound(frequency=800, duration_ms=150, volume=0.4)  # 高音弥
    print("✓ 音效创建成功！")
except Exception as e:
    print(f"✗ 音效创建失败: {e}")
    move_sound = None
    collect_sound = None

# ========== 游戏变量 ==========
player_x = 375
player_y = 275
player_speed = 5
enemy_x = 400
enemy_y = 300
enemy_size = 40
enemy_speed = 3
stat_time = pygame.time.get_ticks()
game_over = False

# 颜色
BLUE = (100, 150, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 100)
GREEN = (0,255,0)

# 抉夹图标的位置
collectibles = [
    (100, 100), (700, 500), (400, 300),
    (200, 400), (600, 150)
]
score = 0

# 字体 - 使用系统中文字体
try:
    font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    big_font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 48)
    print("✓ 中文字体加载成功！")
except:
    font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 48)
    print("✗ 中文字体加载失败，使用备选字体")

# ========== 游戏主循环 ==========
running = True
while running:
    # ---- 1. 事件处理 ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # ---- 2. 键盘输入与移动 ----
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
        moved = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
        moved = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
        moved = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
        moved = True
    
    # 移动时播放音效
    if moved and move_sound:
        move_sound.play()
    
    # 边界限制
    player_x = max(0, min(SCREEN_WIDTH - 50, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - 50, player_y))
    
    # 检测碰撞（收集金币）
    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    for i, pos in enumerate(collectibles):
        item_rect = pygame.Rect(pos[0]-15, pos[1]-15, 30, 30)
        if player_rect.colliderect(item_rect):
            score += 10
            collectibles[i] = (-100, -100)  # 移到画面外
            # 收集时播放音效
            if collect_sound:
                collect_sound.play()
    
    # ---- 3. 绘制 ----
    for y in range(SCREEN_HEIGHT):
        ratio = y/SCREEN_HEIGHT

        r = int(128+ratio*127)
        g = int(ratio*165)
        b = int(128-ratio*128)

        pygame.draw.line(screen,(r,g,b),(0,y),(SCREEN_WIDTH,y))
    
    # 绘制金币/抉夹
    time_now = pygame.time.get_ticks()/500
    brightness = abs(math.sin(time_now))

    gold_color = (255,int(200*brightness),int(100*brightness))

    for pos in collectibles:
        if pos[0] > 0:  # 只绘制未被收集的
            pygame.draw.circle(screen, gold_color, pos, 15)
            pygame.draw.circle(screen, gold_color, pos, 10)
    
    # 绘制玩家图片（或用方块替代）
    if player_img:
        screen.blit(player_img, (player_x, player_y))
    else:
        pygame.draw.rect(screen, (50, 200, 50), (player_x, player_y, 50, 50))
    
    #绘制敌人
    pygame.draw.rect(screen,(255,0,0),(enemy_x,enemy_y,enemy_size,enemy_size))
    
    # 显示分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 显示提示
    hint_text = font.render("方向键/WASD移动，收集金币（带音效）！", True, WHITE)
    screen.blit(hint_text, (250, 20))
    
    # 胜利检测
    if score >= 50:
        win_text = big_font.render("🎉 你赢了！", True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(win_text, text_rect)
    
    #敌人自移动
    enemy_x = 400 + math.sin(pygame.time.get_ticks()/1000)*300

    #检测玩家撞敌人
    enemy_rect = pygame.Rect(enemy_x,enemy_y,enemy_size,enemy_size)
    if player_rect.colliderect(enemy_rect):
        game_over = True
        enemy_x = 400
    
    #显示生存时间
    survival_time = (pygame.time.get_ticks()-stat_time)/1000
    time_text = font.render(f"生存时间：{survival_time:.1f}秒",True,WHITE)
    screen.blit(time_text,(10,50))
    
    # 更新屏幕
    pygame.display.flip()
    
    # ---- 4. 帧率控制 ----
    clock.tick(FPS)

# 退出
pygame.quit()
sys.exit()
