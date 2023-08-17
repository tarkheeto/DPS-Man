import serial
import time

# Setup the COM ports
base_station = serial.Serial('COM30', 9600, timeout=1)  
dynamic_controller = serial.Serial('COM36', 9600, timeout=1)

def get_float_from_port(port):
    """Try reading a line from a port and convert to float."""
    try:
        line = port.readline().decode().strip()
        return float(line)
    except ValueError:
        print(f"Couldn't convert '{line}' to float.")
        return None

while True:
    base_value = get_float_from_port(base_station)
    controller_value = get_float_from_port(dynamic_controller)
    
    if base_value is not None and controller_value is not None:
        delta = int(controller_value - base_value)
        print(f"Base Station Value: {base_value}, Dynamic Controller Value: {controller_value}, Delta: {delta}")
    
    
