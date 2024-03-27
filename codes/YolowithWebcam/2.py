"""
This module is used for detecting objects in a video stream using YOLO.
"""
import math
import time
from ultralytics import YOLO
import cvzone
import cv2
from positionuse import calculate_robot_arm_angles

#cap = cv2.VideoCapture(1)  # For Webcam
#cap = cv2.VideoCapture("..\codes\Videos\motorbikes.mp4")  # For Video


# To take an image from webcam and save it in folder "..\codes\Image"


# cap = cv2.VideoCapture(0)
# cv2.imwrite("..\codes\Images\fruit.jpg", cap.read()[1])
cap = cv2.VideoCapture(r"..\codes\Image\fruits.jpg")  # For Image
cap.set(3, 1280)
cap.set(4, 720)

actual_width = 40  
actual_height = 50 

pixel_to_cm_ratio_width = actual_width / 1280
pixel_to_cm_ratio_height = actual_height / 720
def draw_axes(img):
    height, width = img.shape[:2]
    center_x, center_y = width // 2, height

    # 画X轴
    cv2.line(img, (0, center_y), (width, center_y), (255, 0, 0), 2)

    # 画Y轴
    cv2.line(img, (center_x, 0), (center_x, center_y), (0, 255, 0), 2)

    return img

nearest_object = None
min_distance = float('inf') #store the distance of the nearest object

model = YOLO("../Yolo-Weights/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]# List of class names


actual_width = 40  
actual_height = 50 

image_width = 1280
image_height = 720

#calculate the pixel to cm ratio
pixel_to_cm_width = actual_width / image_width
pixel_to_cm_height = actual_height / image_height

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        break  # Skip the rest of the loop
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Class Name
            cls = int(box.cls[0])
            className = classNames[cls]

            # Only process apples and bottles
            if className not in ["backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",  "sports ball", "kite",
                                "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
                                "pizza", "donut", "cake",  "pottedplant", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "book",
                                "clock", "vase", "scissors", "hair drier", "toothbrush"
                                ]:# Only process the needed classes
                continue

            

            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            
            
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Get the center of the bounding box
            x_center_cm = ((x1 + x2) / 2) * pixel_to_cm_width - (actual_width / 2)
            y_center_cm = actual_height - ((y1 + y2) / 2) * pixel_to_cm_height
            print(f"The center of {className} is at ({x_center_cm:.2f}, {y_center_cm:.2f}) cm")
            if y_center_cm < min_distance:
                min_distance = y_center_cm
                nearest_object = (x_center_cm, y_center_cm)
            height, width = img.shape[:2]

    draw_axes(img)
    
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # 如果检测到最近的物体，则计算机械臂角度
    if nearest_object:
        angles = calculate_robot_arm_angles(*nearest_object)
        print("Calculated angles for the nearest object:", angles)

    # 在窗口中显示图像
    cv2.imshow("Image", img)
    cv2.imwrite("..\codes\Image\output2.jpg", img)
    cv2.waitKey(1)
    
    # 如果按下空格键则退出循环
    if cv2.waitKey(1) == 32:  
        break

