import cv2
import copy
import numpy as np
from vision.vision import Vision as VS
from strategy.win_strategy import *

# 初始化VS类的一个实例，传入特定的参数
vs = VS(
    mode='test',          # 第一个参数，模式参数。当设置为'test'时，系统将生成并展示中间处理结果或最终的效果图，
                          # 这对于调试和可视化处理流程非常有用。如果设置为'run'，则可能不会生成额外的输出，
                          # 以避免中断正常的程序流程或节省资源。

    blurred_para=1,      # 第二个参数，模糊参数。这可能用于控制图像模糊的程度，例如在进行边缘检测前，
                          # 使用高斯模糊或其他类型的模糊来减少图像噪声。数值越大，模糊效果越强。
                          #可以去除噪声

    edge_para=150,        # 第三个参数，边缘参数。这可能用于控制边缘检测的敏感度或阈值。在Canny边缘检测等算法中，
                          # 较高的值意味着只有非常明显的边缘才会被检测到，较低的值则会检测到更多的边缘细节。
                          #越大中间的矩形越容易被检测到，但过大会导致边缘细节消失
    
    min_distance=50
)

def capture_image():
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    # 读取一帧图像
    ret, frame = cap.read()
    cv2.waitKey(10)

    # 检查是否成功读取帧
    if not ret:
        print("无法获取帧")
        exit()

    height, width, _ = frame.shape
    
    # 计算裁剪的起始和结束位置
    left = int(width * 0.25)
    right = int(width * 0.8)
    top = 0
    bottom = height
    
    # 裁剪图片
    cropped_img = frame[top:bottom, left:right]

    return cropped_img

def compare_board(board_pre, board):
    """
    比较两个棋盘状态，返回是否有棋子被替换
    """
    borad_diff = create_doard()
    start = None
    end = None

    for i in range(9):
        m = i // 3
        n = i % 3
        borad_diff[m][n] = board_pre[m][n] - board[m][n]
    print(f"board_diff:{borad_diff}")
    for i in range(9):
        m = i // 3
        n = i % 3
        if borad_diff[m][n] < 0:
            start = i
        if borad_diff[m][n] > 0:
            end = i
        
    if start is not None and end is not None:
        return start, end
    else:
        return None

# 主函数，负责游戏的运行流程控制
def run():
    # 初始化棋盘状态，直到检测到棋盘的WH尺寸，进入正式的游戏循环
    while vs.WH is None:
        image = capture_image()
        cv2.imshow("image", image)
        cv2.waitKey(10)
        vs.compute_M(image)
        print("WH is None")

    warped = vs.warp_image(image)
    cv2.imshow("warped", warped)
    cv2.waitKey(10)
    original_centers = vs.find_rectangle_centers(warped)
    print(f"original_centers: {original_centers}")
    trans_centers = vs.compute_axis(original_centers)
    print(f"trans_centers: {trans_centers}")
    gray_mean = vs.get_color(image, original_centers)
    vs.gray_mean = gray_mean
    # print(f"gray_mean:{gray_mean}")
    color_codes = vs.get_determine_color(image, original_centers)
    # 在图像上标注每个中心点的颜色和编号
    for i, original_center in enumerate(original_centers):
        cv2.circle(image, (original_center[0], original_center[1]), 5, (0, 0, 255), -1)
        cv2.putText(image, str(color_codes[i]), (original_center[0] - 10, original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image, str(i), (original_center[0], original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("image1", image)
    cv2.waitKey(10)

    # 等待用户输入，确认本次下棋操作完成
    flag = int(input("输入1表示已完成本次下棋: "))
    ch_flag = 1
    for i in range(10):
        image = capture_image()
    color_codes = vs.get_determine_color(image, original_centers)

    # 检查是否有棋子被下，如果没有则认为本次操作没有改变棋盘状态
    for i in range(len(color_codes)):
        if color_codes[i] != 0:
            ch_flag = ch_flag - 1
    start_game(ch_flag)

    board_pre = create_doard()
    board = create_doard()
    while True:
        for i in range(10):
            image1 = capture_image()
        # 检查捕捉到的图像是否有效，无效则退出程序
        if image1 is None or image1.size == 0:
            print("Image1 is empty!")
            exit()
        color_codes = vs.get_determine_color(image1, original_centers)
        # 在图像上标注每个中心点的颜色和编号
        for i, original_center in enumerate(original_centers):
            cv2.circle(image1, (original_center[0], original_center[1]), 5, (0, 0, 255), -1)
            cv2.putText(image1, str(color_codes[i]), (original_center[0] - 10, original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image1, str(i), (original_center[0], original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imshow("image_put", image1)
        cv2.waitKey(10)
        # 更新棋盘状态
        for i in range(len(color_codes)):
            board[i // 3][i % 3] = color_codes[i]
        
        #对比board_pre和board
        if compare_board(board_pre, board) is not None:
            start, end = compare_board(board_pre, board)
            print("board changed!")
            print(f"board change,you should move: start: {start}, end: {end}")
        else:
            # 检查游戏是否结束
            if game_over(board):
                print("Game Over!")
                break

            # 电脑进行下一步操作
            row, col = computer_move(board)
            board[row][col] = Piece.X
            print("computer move:", row, col)
            #更新board_pre状态
            board_pre = copy.deepcopy(board)

        print(f"board:{board}")

        # 等待用户输入，确认本次下棋操作完成
        flag = int(input("输入1表示已完成本次下棋: "))

    # 输出游戏结果
    print("game over!result:")
    for row in board:
        print(row)
    print("winner:", evaluate(board))


if __name__ == '__main__':
    # 打开默认摄像头，通常索引为0
    cap = cv2.VideoCapture(0)
    run()