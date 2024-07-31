import pygame

# 初始化pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((800, 450))

# 设置颜色
MILK_COLOUR = (255, 200, 238)  # 米黄色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置字体
font = pygame.font.Font(None, 36)

# 棋盘状态
board = [
    [2, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

# 数字键盘状态
num_center = (600, 100)
num_keyboard = {
    '1': (num_center[0] - 50, num_center[1] - 50),
    '2': (num_center[0], num_center[1] - 50),
    '3': (num_center[0] + 50, num_center[1] - 50),
    '4': (num_center[0] - 50, num_center[1]),
    '5': (num_center[0], num_center[1]),
    '6': (num_center[0] + 50, num_center[1]),
    '7': (num_center[0] - 50, num_center[1] + 50),
    '8': (num_center[0], num_center[1] + 50),
    '9': (num_center[0] + 50, num_center[1] + 50),
}

# 确定和删除按钮状态
buttons = {
    'OK': (num_center[0] - 30, num_center[1] + 100),
    'DEL': (num_center[0] + 30, num_center[1] + 100),
}

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击位置
            x, y = pygame.mouse.get_pos()
            if 510 <= x <= 590 and 350 <= y <= 390:  # 确定按钮
                print("确定")
            elif 550 <= x <= 590 and 350 <= y <= 390:  # 删除按钮
                print("删除")
            else:
                for num, pos in num_keyboard.items():  # 数字键盘
                    if pos[0] <= x <= pos[0] + 40 and pos[1] <= y <= pos[1] + 40:
                        print(f"数字: {num}")
    
    # 填充背景色
    screen.fill(MILK_COLOUR)
    
    # 绘制棋盘
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(i * 100, j * 100, 100, 100)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[i][j] == 2:
                pygame.draw.circle(screen, BLACK, (i * 100 + 50, j * 100 + 50), 40)
            elif board[i][j] == 1:
                pygame.draw.circle(screen, WHITE, (i * 100 + 50, j * 100 + 50), 40)
    
    # 绘制数字键盘和按钮
    for num, pos in num_keyboard.items():
        text = font.render(num, True, BLACK)
        screen.blit(text, pos)
    for btn, pos in buttons.items():
        text = font.render(btn, True, BLACK)
        screen.blit(text, pos)
    
    # 更新屏幕
    pygame.display.flip()

# 退出pygame
pygame.quit()