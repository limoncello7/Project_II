import math
import time
from ultralytics import YOLO
import cvzone
import cv2
import serial
from positionuse import calculate_robot_arm_angles

cap = cv2.VideoCapture(r"..\codes\Image\fruits.jpg")  # For Image
cap.set(3, 1280)
cap.set(4, 720)

actual_width = 80
actual_height = 50 

pixel_to_cm_ratio_width = actual_width / 1280
pixel_to_cm_ratio_height = actual_height / 720
def draw_axes(img):
    height, width = img.shape[:2]
    center_x, center_y = width // 2, height


    cv2.line(img, (0, center_y), (width, center_y), (255, 0, 0), 2)


    cv2.line(img, (center_x, 0), (center_x, center_y), (0, 255, 0), 2)

    return img
nearest_object = None
nearest_distance = float('inf')
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
              ]



objects_within_grasp = []

image_width = 1280
image_height = 720

pixel_to_cm_width = actual_width / image_width
pixel_to_cm_height = actual_height / image_height

prev_frame_time = 0
new_frame_time = 0



while True:
    new_frame_time = time.time()    
    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        break

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            className = classNames[int(box.cls[0])]
            if className not in [ "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",  "sports ball", "kite",
                                "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
                                "pizza", "donut", "cake",  "pottedplant", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "book",
                                "clock", "vase", "scissors", "hair drier", "toothbrush"
                                ]:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            cvzone.cornerRect(img, (x1, y1, w, h))
            conf = math.ceil((box.conf[0] * 100)) / 100
            cvzone.putTextRect(img, f'{classNames[int(box.cls[0])]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            x_center_pixels = (x1 + x2) / 2
            y_center_pixels = (y1 + y2) / 2
            # Calculate center in cm and distance
            x_center_cm = ((x1 + x2) / 2) * pixel_to_cm_ratio_width - (actual_width / 2)
            y_center_cm = ( y_center_pixels * pixel_to_cm_ratio_height)
            distance = math.sqrt(x_center_cm**2 + y_center_cm**2)

            # Assume calculate_robot_arm_angles now also calculates and returns the angle to the object
            angle1, angle2, angle3 = calculate_robot_arm_angles(x_center_cm, y_center_cm)
            # Check if the object is within the graspable angle range and add it to a list
            angle=(angle1,angle2,angle3)
            if (0 <= angle1 and angle1 <= 180) and (0.5 <= angle2 and angle2 <= 125) and (0 <= angle3 and angle3 <= 155):
                objects_within_grasp.append((distance, (x_center_cm, y_center_cm), angle))
    draw_axes(img)
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    # Find the nearest object within the graspable range
    if objects_within_grasp:
        nearest_distance, nearest_object, _ = min(objects_within_grasp, key=lambda x: x[0])

    if nearest_object:
        base_angle, rear_arm_angle, front_arm_angle = angle  

        arduino = serial.Serial('COM3', 9600) 
        
        time.sleep(3) 

        arduino.write(f'b{base_angle}'.encode()+b'\n')
        time.sleep(1) 
        arduino.write(f'r{rear_arm_angle}'.encode()+b'\n')
        time.sleep(1)
        arduino.write(f'f{front_arm_angle}'.encode()+b'\n')
        time.sleep(0.5)
    while arduino.inWaiting() > 0:  
        received_data = arduino.readline().decode().strip()  
        print(f"{received_data}")  
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 32:
        break
