# Pygame 学习之旅 🎮

系统性学习 Pygame 游戏开发的完整路径。

## 学习进度

| 步骤 | 名称 | 主要内容 | 状态 |
|------|------|---------|------|
| **Step 1** | 窗口创建 | 创建窗口、游戏循环、图片加载 | ✅ 完成 |
| **Step 2** | 键盘控制 | 方向键控制、边界限制、基础碰撞 | ✅ 完成 |
| **Step 3** | 渐变与动画 | 渐变背景、时间驱动动画、程序化音效 | ✅ 完成 |
| **Step 4** | Sprite 系统 | 精灵类、精灵组、游戏状态机、最高分存档 | ✅ 完成 |
| **Step 5** | 打砖块 | 球物理、角度反射、砖块数组、生命系统 | ✅ 完成 |

---

## 目录结构

```
pygame_learning/
├── README.md                      # 本文件
├── step1_window/                  # 第一步：窗口创建
│   ├── step1_window.py            # 基础窗口创建
│   └── step1_images.py            # 图片加载版本
├── step2_keyboard/               # 第二步：键盘控制
│   └── step2_keyboard_control.py  # 方向键控制练习
├── step3_gradient/               # 第三步：渐变与动画
│   ├── gradient_practice.py       # 渐变练习
│   ├── animation_practice.py      # 动画练习
│   ├── sound_practice.py          # 音效练习
│   └── mini_game.py               # 小游戏综合
├── step4_sprite/                 # 第四步：Sprite 系统
│   └── step4_sprite_game.py       # Sprite 重构版游戏
└── step5_breakout/               # 第五步：打砖块
    ├── practice1_basics.py        # 练习1: 基础框架
    ├── practice2_angle_bounce.py  # 练习2: 角度反射
    ├── practice3_bricks.py        # 练习3: 砖块数组
    └── breakout_complete.py       # 完整版游戏
```

---

## 快速开始

### 运行环境
```bash
# 激活虚拟环境
source ~/gamedev/bin/activate

# 或者直接使用完整路径
~/gamedev/bin/python stepX/xxx.py
```

### 按步骤学习
建议从 Step 1 开始，逐步完成每个练习。

---

## 技能树

```
Pygame 基础
├── 窗口管理 [Step 1]
├── 键盘输入 [Step 2]
├── 图形绘制 [Step 1-2]
├── 渐变效果 [Step 3]
├── 动画原理 [Step 3]
├── 音效处理 [Step 3]
├── Sprite 系统 [Step 4]
├── 碰撞检测 [Step 2,4,5]
├── 游戏状态 [Step 4,5]
└── 物理运动 [Step 5]
    └── 角度反射 [Step 5]
```

---

## 学习日志

- **Day 1** (5月5日): 完成 Step 1 - 窗口创建
- **Day 2** (5月9日): 完成 Step 3 - 渐变、动画、音效
- **Day 3** (5月11日): 完成 Step 4 - Sprite 系统
- **Day 4** (5月12日): 完成 Step 5 - 打砖块

---

## 学习建议

1. **先跑起来**: 每个练习都是可独立运行的，先让代码跑起来，再理解原理
2. **填空式学习**: Step 5 的练习采用填空式，先自己尝试填写，再对照答案
3. **修改尝试**: 每完成一个练习，尝试修改参数（颜色、速度、大小）看看效果
4. **综合项目**: 完成所有步骤后，尝试独立完成一个完整游戏

---

## 常用命令

```bash
# 运行特定步骤的代码
~/gamedev/bin/python step1_window/step1_window.py
~/gamedev/bin/python step2_keyboard/step2_keyboard_control.py
~/gamedev/bin/python step3_gradient/mini_game.py
~/gamedev/bin/python step4_sprite/step4_sprite_game.py
~/gamedev/bin/python step5_breakout/breakout_complete.py
```

---

**享受编程，享受创造！** 🎮✨
