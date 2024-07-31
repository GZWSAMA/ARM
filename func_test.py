import cv2
import numpy as np

def compute_axis(centers):
    box = np.array([
        [99, 226], [98, 301], [98, 377], [247, 375]
    ], dtype="float32")
    # 重新计算目标点
    dst_pts = np.array([
        [161,-31],
        [161,28],
        [224,-29],
        [224,30]
    ], dtype="float32")

    # 计算透视变换矩阵
    M_trans = cv2.getPerspectiveTransform(box, dst_pts)

    trans_centers = []
    for center in centers:
        # 已知变换后的点坐标
        transformed_point = np.array([center[0], center[1]])
        # 将点坐标转换为齐次坐标
        homogeneous_point = np.array([[transformed_point[0]], [transformed_point[1]], [1]])
        # 执行逆透视变换
        original_point_homogeneous = Minv @ homogeneous_point
        w = original_point_homogeneous[2]
        trans_point = (int(original_point_homogeneous[0] / w), int(original_point_homogeneous[1] / w))
        trans_centers.append(trans_point)
    return trans_centers