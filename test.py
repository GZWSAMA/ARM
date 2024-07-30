import cv2
import numpy as np
from vision.vision import Vision as VS

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

    return frame

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

def run():
    # while vs.WH is None:
    #     image = capture_image()
    #     cv2.imshow("image", image)
    #     cv2.waitKey(10)
    #     vs.compute_M(image)
    #     print("WH is None")

    # image = cv2.imread("./datas/8.jpg")
    for i in range(10):
        image = capture_image()
    while vs.WH is None:
        vs.compute_M(image)
        print("WH is None")

    # image = capture_image()
    if image is None or image.size == 0:
        print("Image is empty!")
        exit()

    print(vs.M)

    warped = vs.warp_image(image)
    if warped is None or warped.size == 0:
        print("warped is empty!")
        exit()
    cv2.imshow("warped", warped)
    cv2.waitKey(10)

    original_centers = vs.find_rectangle_centers(warped)
    print(f"original_centers{original_centers}")
    color_codes = vs.get_determine_color(image, original_centers)
    print(f"color_codes{color_codes}")
    for i,original_center in enumerate(original_centers):
        cv2.circle(image, (original_center[0], original_center[1]), 5, (0, 0, 255), -1)
        cv2.putText(image, str(color_codes[i]), (original_center[0] - 10, original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image, str(i), (original_center[0], original_center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("image", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    # 打开默认摄像头，通常索引为0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    run()