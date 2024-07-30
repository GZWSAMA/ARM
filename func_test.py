import cv2

# 创建VideoCapture对象
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 调整摄像头参数
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 1.5)  # 降低亮度
# cap.set(cv2.CAP_PROP_EXPOSURE, -5)     # 降低曝光
# cap.set(cv2.CAP_PROP_CONTRAST, 0.5)    # 增加对比度
cap.set(cv2.CAP_PROP_AUTO_WB, 1)       # 关闭自动白平衡

# # 手动设置白平衡
# # 注意：并非所有摄像头都支持直接设置白平衡
# try:
#     cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 4000)
#     cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, 4000)
# except Exception as e:
#     print("Warning: Could not set white balance. Error:", str(e))

while True:
    # 读取摄像头的一帧图像
    ret, frame = cap.read()

    if not ret:
        break

    # 显示图像
    cv2.imshow('frame', frame)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()