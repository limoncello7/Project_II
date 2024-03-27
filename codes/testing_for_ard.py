import serial
import time


arduino = serial.Serial('COM3', 9600)  
time.sleep(2)  

user_input = input("请输入要发送的文本：")


arduino.write(user_input.encode() + b'\n')  
time.sleep(0.1)


while arduino.inWaiting() > 0:
    received_data = arduino.readline().decode().strip()  
    print(f"Received: {received_data}") 

arduino.close()
