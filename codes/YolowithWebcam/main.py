import cv2
from ultralytics import YOLO
import numpy as np

# 初始化 YOLO 模型
model = YOLO("../Yolo-Weights/yolov8l.pt")

# 直接读取图像
img = cv2.imread(r"..\codes\Runningyolo\Images\fruit2.jpg")

# 图像中心
image_center = np.array([img.shape[1] / 2, img.shape[0] / 2])

# 进行物体检测
results = model(img)

min_distance = float('inf')
nearest_object_coordinates = None

# 正确访问检测结果
for det in results.xyxy[0]:  # 遍历每个检测到的物体
    x_center = (det[0] + det[2]) / 2
    y_center = (det[1] + det[3]) / 2
    object_center = np.array([x_center, y_center])

    # 计算到图像中心的距离
    distance = np.linalg.norm(image_center - object_center)

    # 更新最近物体的信息
    if distance < min_distance:
        min_distance = distance
        nearest_object_coordinates = (x_center, y_center)

if nearest_object_coordinates:
    print("最近物体的坐标:", nearest_object_coordinates)
