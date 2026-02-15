# save as find_ports.py
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
print("--- AVAILABLE PORTS ---")
for port, desc, hwid in ports:
    print(f"{port}: {desc}")