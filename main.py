import multiprocessing
import subprocess
import time
import os
import sys

# --- CONFIG ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def run_ui():
    """1. The Display (The Brain)"""
    print("[SYSTEM] Launching Interface...")
    subprocess.run([sys.executable, "computer_vision/virtual_giftbox.py"])

def run_vision():
    """2. The Camera (The Eyes)"""
    time.sleep(2) 
    print("[SYSTEM] Launching Vision Sensor...")
    subprocess.run([sys.executable, "computer_vision/emotion_sender.py"])

def run_bio():
    """3. The Arduino (The Pulse)"""
    time.sleep(3) 
    print("[SYSTEM] Connecting to Arduino GSR...")
    subprocess.run([sys.executable, "computer_vision/arduino_bridge.py"])

def run_esp_face():
    """4. The Face (ESP8266 Display Animation)"""
    time.sleep(4) # Wait for other systems to initialize
    print("[SYSTEM] Launching ESP8266 Face Bridge...")
    subprocess.run([sys.executable, "esp_face_bridge.py"])

if __name__ == "__main__":
    print("--- PRESAGE ALL-IN-ONE SYSTEM START ---")
    print("Type Ctrl+C to Stop All Systems")

    # Define all four subsystems
    p_ui = multiprocessing.Process(target=run_ui)
    p_vision = multiprocessing.Process(target=run_vision)
    p_bio = multiprocessing.Process(target=run_bio)
    p_face = multiprocessing.Process(target=run_esp_face)

    # Launch all processes
    p_ui.start()
    p_vision.start()
    p_bio.start()
    p_face.start()

    try:
        # Keep main script alive and wait for all processes
        p_ui.join()
        p_vision.join()
        p_bio.join()
        p_face.join()
    except KeyboardInterrupt:
        print("\n[SYSTEM] SHUTTING DOWN...")
        # Terminate everything on exit
        p_ui.terminate()
        p_vision.terminate()
        p_bio.terminate()
        p_face.terminate()
        print("[SYSTEM] All sensors and display bridges offline.")