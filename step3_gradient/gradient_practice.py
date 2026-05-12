"""
Pygame Step 3 - 渐变背景练习
============================
学习目标: 掌握颜色插值原理

核心公式:
    color = start_color + (end_color - start_color) * ratio

在标注 "#在这里填空" 的地方填写代码
"""

import pygame

# ========== 初始化 ==========
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("渐变背景练习 - 按 R 重置")

clock = pygame.time.Clock()

# 定义颜色
WHITE = (255, 255, 255)

# ========== 渐变配置 ==========
# 从深蓝 (0, 0, 100) 渐变到浅蓝 (100, 150, 255)
START_COLOR = (0, 0, 100)      # 顶部颜色
END_COLOR = (100, 150, 255)    # 底部颜色

# 测试用的第二组渐变（按空格键切换）
# 紫色 (128, 0, 128) 到橙色 (255, 165, 0)
START_COLOR_2 = (128, 0, 128)
END_COLOR_2 = (255, 165, 0)

# 当前使用的渐变
start_color = START_COLOR
end_color = END_COLOR

def draw_gradient(screen, start_c, end_c):
    """
    绘制垂直渐变背景
    参数:
        screen: Pygame 窗口
        start_c: 顶部颜色 (r, g, b)
        end_c: 底部颜色 (r, g, b)
    """
    width, height = screen.get_size()
    
    # 遍历每一行像素
    for y in range(height):
        # 计算当前行的比例 (0.0 ~ 1.0)
        # 顶部 y=0 时 ratio=0，底部 y=height-1 时 ratio=1
        ratio = y / height
        
        # 在这里填空！
        # 提示: r = start_r + (end_r - start_r) * ratio
        # 注意转换为 int！
        
        # ========== 在这里填空 ==========
        r = int(start_color[0]+ratio*(end_color[0]-start_color[0]))  # 红色通道
        g = int(start_color[1]+ratio*(end_color[1]-start_color[1]))  # 绿色通道  
        b = int(start_color[2]+ratio*(end_color[2]-start_color[2]))  # 蓝色通道
        # ================================
        
        # 绘制一条水平线
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))


# ========== 游戏循环 ==========
running = True
show_hint = True  # 显示提示文字

while running:
    # 1. 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # 按空格切换渐变配色
            if event.key == pygame.K_SPACE:
                if start_color == START_COLOR:
                    start_color = START_COLOR_2
                    end_color = END_COLOR_2
                else:
                    start_color = START_COLOR
                    end_color = END_COLOR
            
            # 按 H 隐藏/显示提示
            if event.key == pygame.K_h:
                show_hint = not show_hint
            
            # 按 R 重置
            if event.key == pygame.K_r:
                start_color = START_COLOR
                end_color = END_COLOR
    
    # 2. 绘制
    # 绘制渐变背景
    draw_gradient(screen, start_color, end_color)
    
    # 显示提示文字
    if show_hint:
        font = pygame.font.SysFont("arial", 24)
        
        # 背景提示
        bg_text = font.render(f"Gradient: {start_color} -> {end_color}", True, WHITE)
        screen.blit(bg_text, (10, 10))
        
        # 操作说明
        controls = [
            "SPACE: Switch gradient",
            "H: Hide/Show hints", 
            "R: Reset",
            "Fill in the blanks in draw_gradient()!"
        ]
        for i, text in enumerate(controls):
            surface = font.render(text, True, WHITE)
            screen.blit(surface, (10, 50 + i * 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
