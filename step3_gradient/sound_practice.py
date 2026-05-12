"""
Pygame Step 3 - 无依赖音效练习
============================
学习目标: 用纯 Python 生成正弦波音效

核心公式:
    sample = volume * sin(2π * frequency * time)
"""

import pygame
import array
import math

# ========== 初始化 ==========
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("音效练习 - 数字键 1-4 播放音效")

clock = pygame.time.Clock()
font = pygame.font.SysFont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)

# ========== 在这里填空 - 音效生成函数 ==========

def create_tone(frequency=440, duration_ms=100, volume=0.3):
    """
    生成正弦波音效
    参数:
        frequency: 频率(Hz)，越高越尖锐
        duration_ms: 持续时间(毫秒)
        volume: 音量 0.0~1.0
    返回:
        pygame.mixer.Sound 对象
    """
    sample_rate = 44100
    samples = int(sample_rate * duration_ms / 1000)
    buf = array.array('h')  # 有符号短整数
    
    max_val = int(32767 * volume)
    
    for i in range(samples):
        t = i / sample_rate  # 当前时间(秒)
        
        # 在这里填空！
        # 正弦波公式: sin(2 * pi * frequency * t)
        # ========== 在这里填空 ==========
        val = int(max_val * math.sin(2 * math.pi * frequency * t))
        # ================================
        
        buf.append(val)
    
    return pygame.mixer.Sound(buffer=buf)


# ========== 创建预设音效 ==========

# 练习1: 移动音 (低沉短促, 300Hz, 50ms)
# ========== 在这里填空 ==========
move_sound = create_tone(300,50,0.3)
# ================================

# 练习2: 收集音 (高亮清脇, 880Hz, 150ms, 音量0.4)
# ========== 在这里填空 ==========
collect_sound = create_tone(880,150,0.4)
# ================================

# 练习3: 碰撞音 (粗糙低音, 150Hz, 200ms, 音量0.5)
# ========== 在这里填空 ==========
collision_sound = create_tone(150,200,0.5)
# ================================

# 提供的胜利音阶 (已完成，供参考)
def create_victory_sound():
    """播放胜利音阶 C-E-G-C"""
    notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
    for note in notes:
        sound = create_tone(note, 200, 0.3)
        sound.play()
        pygame.time.wait(200)

# ========== 游戏状态 ==========
player_x = 400
player_y = 300
player_size = 40
speed = 5

coins = [
    pygame.Rect(200, 200, 30, 30),
    pygame.Rect(600, 200, 30, 30),
    pygame.Rect(200, 400, 30, 30),
    pygame.Rect(600, 400, 30, 30),
]

score = 0

# ========== 游戏循环 ==========
running = True
show_hint = True

while running:
    # 1. 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # 数字键测试音效
            if event.key == pygame.K_1:
                move_sound.play()
            elif event.key == pygame.K_2:
                collect_sound.play()
            elif event.key == pygame.K_3:
                collision_sound.play()
            elif event.key == pygame.K_4:
                create_victory_sound()
            elif event.key == pygame.K_h:
                show_hint = not show_hint
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # 2. 更新游戏
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_LEFT]:
        player_x -= speed
        moved = True
    if keys[pygame.K_RIGHT]:
        player_x += speed
        moved = True
    if keys[pygame.K_UP]:
        player_y -= speed
        moved = True
    if keys[pygame.K_DOWN]:
        player_y += speed
        moved = True
    
    # 移动时播放音效 (限制频率)
    if moved and pygame.time.get_ticks() % 10 == 0:
        move_sound.play()
    
    # 边界限制
    player_x = max(player_size, min(SCREEN_WIDTH - player_size, player_x))
    player_y = max(player_size, min(SCREEN_HEIGHT - player_size, player_y))
    
    # 碰撞检测
    player_rect = pygame.Rect(player_x - player_size//2, player_y - player_size//2, 
                              player_size, player_size)
    
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 10
            collect_sound.play()
    
    # 重生金币
    if len(coins) == 0:
        coins = [
            pygame.Rect(200, 200, 30, 30),
            pygame.Rect(600, 200, 30, 30),
            pygame.Rect(200, 400, 30, 30),
            pygame.Rect(600, 400, 30, 30),
        ]
        create_victory_sound()
    
    # 3. 绘制
    screen.fill((30, 30, 60))
    
    # 绘制金币
    time_ms = pygame.time.get_ticks()
    for coin in coins:
        # 闪烁效果
        brightness = abs(math.sin(time_ms / 300))
        gold_color = (255, int(200 * brightness), int(50 * brightness))
        pygame.draw.circle(screen, gold_color, coin.center, 15)
    
    # 绘制玩家
    pygame.draw.rect(screen, (80, 200, 80), player_rect)
    
    # 显示UI
    score_text = font.render(f"分数: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    if show_hint:
        hints = [
            "方向键: 移动角色",
            "1: 移动音 (300Hz)",
            "2: 收集音 (880Hz)",
            "3: 碰撞音 (150Hz)",
            "4: 胜利音阶",
            "H: 隐藏提示",
            "",
            "任务: 填充以上空白处完成音效生成!"
        ]
        for i, text in enumerate(hints):
            surface = font.render(text, True, (200, 200, 200))
            screen.blit(surface, (10, 50 + i * 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
