"""
Pygame Step 3 - 综合练习: 迷你躲避游戏
================================
用今天学的所有技能创建一个完整游戏！

必须包含:
1. 渐变背景
2. 摇摆的敌人 (sin动画)
3. 闪烁的金币 (abs(sin))
4. 音效反馈 (移动/收集/碰撞)
5. 碰撞检测
6. 游戏结束和重启
"""

import pygame
import array
import math

# ========== 在这里填写初始化代码 ==========
# 提示: pygame.init(), pygame.mixer.init(), set_mode, set_caption

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("迷你躲避游戏 - 方向键移动，R重启")

clock = pygame.time.Clock()

# 加载中文字体
font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
big_font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 48)

# ========== 在这里填写音效生成函数 ==========
# 参考之前的 create_tone 函数

def create_tone(frequency=440, duration_ms=100, volume=0.3):
    """生成正弦波音效"""
    sample_rate = 44100
    samples = int(sample_rate * duration_ms / 1000)
    buf = array.array('h')
    max_val = int(32767 * volume)
    
    for i in range(samples):
        t = i / sample_rate
        val = int(max_val * math.sin(2 * math.pi * frequency * t))
        buf.append(val)
    
    return pygame.mixer.Sound(buffer=buf)

# 创建音效
move_sound = create_tone(300, 50, 0.2)
collect_sound = create_tone(880, 100, 0.3)
collision_sound = create_tone(150, 300, 0.5)

# ========== 游戏状态 ==========
player_x = 100
player_y = 300
player_size = 40
player_speed = 5

enemy_y = 300
enemy_base_x = 400
enemy_range = 200
enemy_size = 50

score = 0
game_over = False
start_time = 0

# 创建金币
coins = []
for i in range(4):
    x = 250 + i * 150
    y = 150 if i % 2 == 0 else 450
    coins.append({
        'rect': pygame.Rect(x - 15, y - 15, 30, 30),
        'collected': False
    })

# ========== 游戏循环 ==========
running = True

while running:
    # 1. 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # 重启游戏
            if event.key == pygame.K_r and game_over:
                game_over = False
                player_x = 100
                player_y = 300
                score = 0
                start_time = pygame.time.get_ticks()
                # 重置金币
                for coin in coins:
                    coin['collected'] = False
    
    # 2. 更新游戏 (只在未结束时)
    if not game_over:
        # 获取时间
        time_ms = pygame.time.get_ticks()
        if start_time == 0:
            start_time = time_ms
        
        # 玩家移动
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            moved = True
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            moved = True
        if keys[pygame.K_UP]:
            player_y -= player_speed
            moved = True
        if keys[pygame.K_DOWN]:
            player_y += player_speed
            moved = True
        
        # 播放移动音效 (限制频率)
        if moved and time_ms % 15 == 0:
            move_sound.play()
        
        # 边界限制
        player_x = max(player_size, min(SCREEN_WIDTH - player_size, player_x))
        player_y = max(player_size, min(SCREEN_HEIGHT - player_size, player_y))
        
        # ========== 在这里填写敌人摇摆 ==========
        # 目标: 敌人在 enemy_base_x 左右 enemy_range 范围内摇摆
        # 提示: enemy_x = enemy_base_x + sin(time / 1000) * enemy_range
        enemy_x = enemy_base_x + math.sin(time_ms/1000)*enemy_range
        
        # ========== 在这里填写碰撞检测 ==========
        # 提示: 创建 player_rect 和 enemy_rect，使用 colliderect 检测
        player_rect = pygame.Rect(player_x,player_y,player_size,player_size)
        enemy_rect = pygame.Rect(enemy_x,enemy_y,enemy_size,enemy_size)
        
        if player_rect.colliderect(enemy_rect):
            game_over = True
            collision_sound.play()
            survival_time = (time_ms - start_time) / 1000
        
        # ========== 在这里填写金币收集 ==========
        # 提示: 遍历金币，检测 colliderect，播放音效，增加分数
        for coin in coins:
            if not coin['collected'] and player_rect.colliderect(coin['rect']):
                coin['collected'] = True
                collect_sound.play()  # 播放音效
                score += 10  # 增加分数
    
    # 3. 绘制
    # ========== 在这里填写渐变背景 ==========
    # 从 (0, 0, 100) 渐变到 (100, 150, 255)
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(ratio*100)
        g = int(ratio*150)
        b = int(100+ratio*155)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    if not game_over:
        # 绘制金币 (闪烁效果)
        time_ms = pygame.time.get_ticks()
        for coin in coins:
            if not coin['collected']:
                # ========== 在这里填写闪烁效果 ==========
                brightness = abs(math.sin(time_ms/300))  # abs(sin(time/300))
                gold_color = (255, int(200 * brightness), int(50 * brightness))
                
                pygame.draw.circle(screen, gold_color, coin['rect'].center, 15)
        
        # 绘制敌人
        pygame.draw.rect(screen, (255, 80, 80), 
                        (enemy_x - enemy_size//2, enemy_y - enemy_size//2, 
                         enemy_size, enemy_size))
        # 敌人眼睛
        pygame.draw.rect(screen, (50, 0, 0), 
                        (enemy_x - 12, enemy_y - 8, 8, 8))
        pygame.draw.rect(screen, (50, 0, 0), 
                        (enemy_x + 4, enemy_y - 8, 8, 8))
        
        # 绘制玩家
        pygame.draw.rect(screen, (80, 200, 80), 
                        (player_x - player_size//2, player_y - player_size//2,
                         player_size, player_size))
        
        # 显示分数
        score_text = font.render(f"分数: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
    else:
        # 游戏结束画面
        game_over_text = big_font.render("游戏结束!", True, (255, 80, 80))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(game_over_text, text_rect)
        
        final_score = font.render(f"最终分数: {score}", True, (255, 255, 255))
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        screen.blit(final_score, score_rect)
        
        time_text = font.render(f"生存时间: {survival_time:.1f}秒", True, (200, 200, 200))
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        screen.blit(time_text, time_rect)
        
        restart_text = font.render("按 R 重新开始", True, (255, 255, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
