"""
Step 4 任务 1：Sprite 系统重构
用 pygame.sprite.Sprite 重写躲球游戏
"""

import pygame
import sys
import math
import os

# ========== 初始化 ==========
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (100, 150, 255)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
GREEN = (50, 200, 50)
YELLOW = (255, 215, 0)
GOLD = (255, 180, 50)
BLACK = (0, 0, 0)

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite 重构版 - 躲避球")
clock = pygame.time.Clock()

# 字体
try:
    font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    big_font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 48)
except:
    font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 48)


# ========== 精灵类定义 ==========

class Player(pygame.sprite.Sprite):
    """玩家精灵：用方向键或 WASD 控制"""
    
    def __init__(self):
        super().__init__()
        # 创建玩家图像（绿色笑脸）
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (25, 25), 25)
        pygame.draw.circle(self.image, (30, 150, 30), (25, 25), 20)
        # 眼睛
        pygame.draw.circle(self.image, WHITE, (17, 20), 6)
        pygame.draw.circle(self.image, WHITE, (33, 20), 6)
        pygame.draw.circle(self.image, BLACK, (17, 20), 3)
        pygame.draw.circle(self.image, BLACK, (33, 20), 3)
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed = 5
    
    def update(self):
        """每帧自动调用：处理键盘输入和移动"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # 边界限制（保持在屏幕内）
        self.rect.clamp_ip(screen.get_rect())


class Enemy(pygame.sprite.Sprite):
    """敌人精灵：按正弦波轨迹移动"""
    
    def __init__(self, center_x, center_y, amplitude_x=250, amplitude_y=150, speed=0.001):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 40, 40))
        # 危险标记
        pygame.draw.line(self.image, WHITE, (10, 15), (30, 15), 3)
        
        self.rect = self.image.get_rect()
        self.center_x = center_x
        self.center_y = center_y
        self.amplitude_x = amplitude_x
        self.amplitude_y = amplitude_y
        self.speed = speed
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        """每帧自动调用：按时间计算新位置"""
        elapsed = pygame.time.get_ticks() - self.start_time
        
        # 正弦波移动
        offset_x = math.sin(elapsed * self.speed) * self.amplitude_x
        offset_y = math.cos(elapsed * self.speed * 1.5) * self.amplitude_y
        
        self.rect.centerx = int(self.center_x + offset_x)
        self.rect.centery = int(self.center_y + offset_y)


class Coin(pygame.sprite.Sprite):
    """金币精灵：带呼吸闪烁效果"""
    
    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.radius = 15
        self.rect = self.base_image.get_rect()
        self.rect.center = (x, y)
        self.image = self.base_image
    
    def update(self):
        """每帧自动调用：更新闪烁效果"""
        # 呼吸效果：亮度在 0.3 ~ 1.0 之间变化
        brightness = 0.3 + 0.7 * abs(math.sin(pygame.time.get_ticks() / 300))
        
        # 根据亮度重绘
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        gold_color = (255, int(200 * brightness), int(100 * brightness))
        pygame.draw.circle(self.image, gold_color, (15, 15), self.radius)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 10)


class Particle(pygame.sprite.Sprite):
    """粒子效果：用于爆炸、收集反馈等"""
    
    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime=30):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (3, 3), 3)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.age = 0
    
    def update(self):
        """每帧自动调用：移动并淡出"""
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.age += 1
        
        # 淡出效果
        alpha = max(0, 255 - int(255 * self.age / self.lifetime))
        self.image.set_alpha(alpha)
        
        # 生命周期结束则移除
        if self.age >= self.lifetime:
            self.kill()


# ========== 游戏状态管理 ==========

class Game:
    """管理整个游戏状态和流程"""
    
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_GAME_OVER = 3
    
    def __init__(self):
        self.state = self.STATE_MENU
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.high_score = self.load_high_score()
        self.reset()

    def load_high_score(self):
        #加载最高分
        try:
            with open(os.path.expanduser("~/pygame_assets/highscore.txt"),"r") as f:
                return float(f.read().strip())
        except:
            return 0.0
    
    def save_high_score(self,score):
        try:
            os.makedirs(os.path.expanduser("~/pygame_assets"),exist_ok=True)
            with open(os.path.expanduser("~/pygame_assets/highscore.txt"),"w") as f:
                f.write(f"{score:.1f}")
        except:
            pass
    
    def reset(self):
        """重置游戏状态"""
        self.state = self.STATE_MENU
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        
        # 创建玩家
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # 创建敌人
        enemy = Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
        
        # 创建金币
        coin_positions = [
            (150, 150), (650, 150),
            (150, 450), (650, 450),
            (400, 300)
        ]
        for x, y in coin_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
    
    def spawn_particles(self, x, y, color, count=10):
        """在指定位置生成粒子爆炸效果"""
        for _ in range(count):
            angle = math.radians(pygame.time.get_ticks() % 360 + (_ * 360 / count))
            speed = 3 + (_ % 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, color, vx, vy)
            self.particles.add(particle)
            self.all_sprites.add(particle)
    
    def update(self):
        """更新游戏逻辑"""

        if self.state in (self.STATE_MENU,self.STATE_PAUSED,self.STATE_GAME_OVER):
            return
        
        # 更新所有精灵
        self.all_sprites.update()
        
        # 检测玩家与敌人碰撞
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.state = self.STATE_GAME_OVER
            # 爆炸粒子效果
            self.spawn_particles(
                self.player.rect.centerx, 
                self.player.rect.centery, 
                RED, 
                count=20
            )
            #保存最高分
            current_time = self.get_survival_time()
            if current_time > self.high_score:
                self.high_score = current_time
                self.save_high_score(current_time)
        
        # 检测玩家与金币碰撞
        collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collected:
            self.score += 10
            # 收集粒子效果
            self.spawn_particles(coin.rect.centerx, coin.rect.centery, GOLD, count=8)
    
    def get_survival_time(self):
        """获取生存时间（秒）"""
        return (pygame.time.get_ticks() - self.start_time) / 1000
    
    def draw(self, surface):
        """绘制游戏画面"""
        # 渐变背景
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * ratio)
            g = int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * ratio)
            b = int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # 绘制所有精灵
        self.all_sprites.draw(surface)
        
        # UI 显示
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        time_text = font.render(f"生存时间: {self.get_survival_time():.1f}秒", True, WHITE)
        surface.blit(time_text, (10, 50))
        
        hint_text = font.render("方向键/WASD 移动，收集金币，避开红色敌人！", True, WHITE)
        surface.blit(hint_text, (200, 20))

        #绘制菜单画面
        if self.state == self.STATE_MENU:
            title = big_font.render("躲避球游戏",True,YELLOW)
            surface.blit(title,title.get_rect(center=(400,200)))
            hint = font.render("按空格键开始游戏",True,WHITE)
            surface.blit(hint,hint.get_rect(center=(400,350)))
            high_text = font.render(f"历史最高:{self.high_score:.1f}秒",True,YELLOW)
            surface.blit(high_text,high_text.get_rect(center=(400,420)))

        #绘制暂停画面
        if self.state == self.STATE_PAUSED:
            overlay = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            overlay.blit(overlay,(0,0))

            pause_text = big_font.render("暂  停",True,YELLOW)
            surface.blit(pause_text,pause_text.get_rect(center=(400,300)))
        
        # 游戏结束画面
        if self.state == self.STATE_GAME_OVER:
            # 半透明遮罩
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            surface.blit(overlay, (0, 0))
            
            # 结束文字
            over_text = big_font.render("游戏结束！", True, RED)
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            surface.blit(over_text, text_rect)
            
            # 最终得分
            final_text = font.render(
                f"最终得分: {self.score} | 生存时间: {self.get_survival_time():.1f}秒", 
                True, WHITE
            )
            final_rect = final_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            surface.blit(final_text, final_rect)

            high_text = font.render(f"历史最高:{self.high_score:.1f}秒",True,GOLD)
            surface.blit(high_text,high_text.get_rect(center=(400,400)))
            
            # 重新开始提示
            restart_text = font.render("按 R 重新开始", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
            surface.blit(restart_text, restart_rect)


# ========== 主程序 ==========

def main():
    game = Game()
    running = True
    
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.state == Game.STATE_GAME_OVER:
                    game.reset()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    if game.state == Game.STATE_PLAYING:
                        game.state = Game.STATE_PAUSED
                    elif game.state == Game.STATE_PAUSED:
                        game.state = Game.STATE_PLAYING
                if event.key == pygame.K_SPACE and game.state == Game.STATE_MENU:
                    game.state = Game.STATE_PLAYING

        
        # 更新
        game.update()
        
        # 绘制
        game.draw(screen)
        pygame.display.flip()
        
        # 帧率控制
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
