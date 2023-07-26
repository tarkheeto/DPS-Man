import serial
import time

# adjust the COM port and baud rate according to your setup
bluetoothSerial = serial.Serial("COM32", 9600)

while True:
    data = bluetoothSerial.readline().decode()  # read a line from the HC-05, decode it to ASCII
    print(data)
    #time.sleep(0.1)  # optional delay for stability