import cv2
import numpy as np

class Vision:
    def __init__(self, mode='test', edge_para=150, blurred_para=1, min_distance=50, radius=5, gray_mean=150):
        self.mode = mode
        self.blurred_para = blurred_para
        self.edge_para = edge_para
        self.min_distance = min_distance
        self.radius = radius
        self.gray_mean = gray_mean
        self.WH = None
        self.M = None
    
    def filter_close_centers(self, centers, min_distance):
        # 保存过滤后的中点
        filtered_centers = []

        # 遍历所有中点
        for center in centers:
            # 检查该中点是否与已添加的中点距离过近
            if not any(self.distance(center, other) < min_distance for other in filtered_centers):
                filtered_centers.append(center)

        return filtered_centers

    def distance(self, point1, point2):
        # 计算两点之间的欧几里得距离
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def order_points(self, pts):
        """
        排序坐标点
        :param pts: 待排序的坐标点
        :return: 排序后的坐标点
        """
        # 初始化坐标点
        rect = np.zeros((4, 2), dtype="float32")

        # 顶部左角的点具有最小的和，
        # 底部右角的点具有最大的和
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # 计算点的差值，
        # 顶部右角的点将具有最小的差值，
        # 底部左角的点将具有最大的差值
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # 返回排序后的坐标点
        return rect
    def compute_M(self, image):
        """
        计算透视变换矩阵
        :param image: 待处理的图片
        :return: 透视变换矩阵
        """
        warped = None
        # 将图像转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 应用高斯模糊减少噪声
        blurred = cv2.GaussianBlur(gray, (self.blurred_para, self.blurred_para), 0)
        
        # 边缘检测
        edges = cv2.Canny(blurred, 50, self.edge_para, apertureSize=3)
        if self.mode == 'test':
            cv2.imshow("edges", edges)
            cv2.waitKey(10)
            
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 遍历每个轮廓
        for contour in contours:
            # 近似轮廓，使其更接近多边形
            epsilon = 0.003 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # 如果轮廓近似后有4个顶点，且面积大于某个阈值，则认为是矩形
            if len(approx) == 4 and cv2.contourArea(contour) > 1000:
                # 获取四边形的四个顶点坐标
                box = approx.reshape(4, 2).astype("float32")

                # 重新排序顶点
                box = self.order_points(box)

                # 计算原始四边形的宽度和高度
                widthA = np.sqrt(((box[0][0] - box[1][0]) ** 2) + ((box[0][1] - box[1][1]) ** 2))
                widthB = np.sqrt(((box[2][0] - box[3][0]) ** 2) + ((box[2][1] - box[3][1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))

                heightA = np.sqrt(((box[0][0] - box[3][0]) ** 2) + ((box[0][1] - box[3][1]) ** 2))
                heightB = np.sqrt(((box[1][0] - box[2][0]) ** 2) + ((box[1][1] - box[2][1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))

                self.WH = [maxWidth, maxHeight]

                # 定义目标点，这里我们增加一些额外的空间，但要确保比例正确
                # 假设你想在每个边上增加10%的空间
                extraSpace = 0  # 5% extra space
                dst_width = maxWidth * (1 + 2 * extraSpace)
                dst_height = maxHeight * (1 + 2 * extraSpace)

                # 重新计算目标点
                dst_pts = np.array([
                    [0 - maxWidth * extraSpace, 0 - maxHeight * extraSpace],
                    [maxWidth + maxWidth * extraSpace, 0 - maxHeight * extraSpace],
                    [maxWidth + maxWidth * extraSpace, maxHeight + maxHeight * extraSpace],
                    [0 - maxWidth * extraSpace, maxHeight + maxHeight * extraSpace]
                ], dtype="float32")

                # 计算透视变换矩阵
                self.M = cv2.getPerspectiveTransform(box, dst_pts)

    def warp_image(self, image):
        """
        寻找轮廓
        :param image: 待处理的图片
        :return: 透视变换后的图片
        """
        # 执行透视变换
        warped = cv2.warpPerspective(image, self.M, (self.WH[0], self.WH[1]))
        
        return warped

    def sort_and_group_points(self, filtered_centers):
        """
        先按照x坐标从小到大排列，再将其按顺序分为三组，
        每组内按照y坐标从大到小顺序排列，最后输出和输入相同格式的列表。
        :param filtered_centers: 输入的中心点列表，假设为numpy数组形式
        :return: 排序和分组后的中心点列表，与输入格式相同
        """
        # 按x坐标排序
        sorted_centers = filtered_centers[np.argsort(filtered_centers[:, 1])]
        
        # 计算每组的大小
        total_points = len(sorted_centers)
        group_size = -(-total_points // 3)  # 使用负负运算来向上取整

        # 分割成三组
        groups = [sorted_centers[i:i + group_size] for i in range(0, total_points, group_size)]
        
        # 对每组按y坐标从大到小排序
        sorted_groups = [group[np.argsort(group[:, 0])[::1]] for group in groups]
        
        final_sorted_centers = []
        for group in sorted_groups:
            final_sorted_centers.extend(group)
        
        return final_sorted_centers


    def find_rectangle_centers(self, image):
        # 读取图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 应用边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # 筛选矩形轮廓
        rectangles = []
        for contour in contours:
            # 近似轮廓
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # 如果轮廓有4个顶点且面积大于一定阈值，则认为是矩形
            if len(approx) == 4 and cv2.contourArea(contour) > 100:
                rectangles.append(approx)

        # 计算并绘制矩形中点
        centers = []
        for rect in rectangles:
            # 获取矩形的边界框
            x, y, w, h = cv2.boundingRect(rect)

            # 计算矩形的中点
            center_x = x + w // 2
            center_y = y + h // 2
            centers.append([center_x, center_y])

        filtered_centers = self.filter_close_centers(centers, self.min_distance)
        filtered_centers = self.sort_and_group_points(np.array(filtered_centers))
        if self.mode == 'test':
            print(f"len of filtered_centers{len(filtered_centers)}")
            # 绘制过滤后的矩形框和中点
            for center_x, center_y in filtered_centers:
                # 找到对应的矩形轮廓
                for rect in rectangles:
                    x, y, w, h = cv2.boundingRect(rect)
                    if x + w // 2 == center_x and y + h // 2 == center_y:
                        # 绘制矩形框
                        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
                        break

                # 标记中点
                cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

            # 显示结果
            cv2.imshow('Filtered Rectangle Centers', image)
            cv2.waitKey(10)

        # 计算逆变换矩阵
        Minv = np.linalg.inv(self.M)
        print(f"Minv:{Minv}")

        original_centers = []
        for center_point in filtered_centers:  
            # 已知变换后的点坐标
            transformed_point = np.array([center_point[0], center_point[1]])
            # 将点坐标转换为齐次坐标
            homogeneous_point = np.array([[transformed_point[0]], [transformed_point[1]], [1]])
            # 执行逆透视变换
            original_point_homogeneous = Minv @ homogeneous_point
            w = original_point_homogeneous[2]
            original_point = (int(original_point_homogeneous[0] / w), int(original_point_homogeneous[1] / w))

            original_centers.append(original_point)

        return original_centers

    def determine_color(self, average_gray):
        # 设置阈值
        white_threshold = self.gray_mean + 8  # 白色的灰度阈值
        black_threshold = self.gray_mean - 30   # 黑色的灰度阈值

        # 判断颜色
        if average_gray >= white_threshold:
            return 1  # 白色
        elif average_gray <= black_threshold:
            return 2  # 黑色
        else:
            return 0  # 其他颜色

    def get_determine_color(self, image, original_centers):
        color_codes = []
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(f"gray_image:{gray_image}")
        for i, original_center in enumerate(original_centers):
            # 解包中心点坐标
            x, y = original_center

            # 计算点周围像素的平均灰度
            roi = gray_image[max(y-self.radius, 0):min(y+self.radius+1, gray_image.shape[0]), 
                            max(x-self.radius, 0):min(x+self.radius+1, gray_image.shape[1])]
            average_gray = np.mean(roi)
            
            # 判断颜色并输出
            print(f"{i}average_gray:{average_gray}")
            color_code = self.determine_color(average_gray)
            color_codes.append(color_code)

        return color_codes

    def get_color(self, image, original_centers):
        average_grays = []
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(f"gray_image:{gray_image}")
        for i, original_center in enumerate(original_centers):
            # 解包中心点坐标
            x, y = original_center

            # 计算点周围像素的平均灰度
            roi = gray_image[max(y-self.radius, 0):min(y+self.radius+1, gray_image.shape[0]), 
                            max(x-self.radius, 0):min(x+self.radius+1, gray_image.shape[1])]
            average_gray = np.mean(roi)
            
            average_grays.append(average_gray)

        return np.mean(average_grays)