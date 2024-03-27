import cv2
from ultralytics import YOLO
import cvzone
import math
import time

from positionuse import calculate_robot_arm_angles

cap = cv2.VideoCapture(r"..\codes\Image\fruits.jpg") 
cap.set(3, 1280)  
cap.set(4, 720)   

model = YOLO("../Yolo-Weights/yolov8l.pt")  


actual_width = 40  
actual_height = 50  


pixel_to_cm_ratio_width = actual_width / 1280
pixel_to_cm_ratio_height = actual_height / 720

nearest_object = None
min_distance = float('inf')  

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        break
    
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            x_center_cm = ((x1 + x2) / 2) * pixel_to_cm_ratio_width - (actual_width / 2)
            y_center_cm = actual_height - ((y1 + y2) / 2) * pixel_to_cm_ratio_height

     
            if y_center_cm < min_distance:
                min_distance = y_center_cm
                nearest_object = (x_center_cm, y_center_cm)


    if nearest_object:
        #print("Nearest object:", nearest_object)
        angles = calculate_robot_arm_angles(*nearest_object)
        #print("Calculated angles for the nearest object:", angles)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 32:  
        break

cap.release()
cv2.destroyAllWindows()
