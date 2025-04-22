# @FileName :cameraProcess.py
# @Time :2025/4/8 下午3:23
# @Author : SCUT Lu


import cv2
import time
import numpy as np
import multiprocessing
import threading
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import concurrent.futures as futures
import os




class camera_task:
    def __init__(self, NS,pipe, stop_event):

        self.NS = NS
        self.record_save = self.NS.record_save
        self.frameRates = self.NS.frameRates
        self.pipe = pipe
        self.stop_event = stop_event
        # 缓存
        self.imgs_buffer = []
        self.executor = futures.ThreadPoolExecutor(max_workers=1)

        # 打开相机
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Camera not found.")
            self.pipe.send("001")
            return
        print("Camera opened successfully.")

    def run(self):
        num_frames = 0
        start_time = time.time()
        # 读取相机


        while not self.stop_event.is_set():
            try:
                flag, frame = self.cap.read()
                if flag:
                    # 计算帧率
                    num_frames += 1
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        fps = num_frames / elapsed_time
                    else:
                        fps = 0
                    if num_frames > 300:
                        num_frames = 0
                        start_time = time.time()
                    # print("fps:",fps)
                    # print(self.NS)
                    # print(self.record_save)

                    # frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LINEAR)
                    if num_frames % 1 == 0:
                        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # frame_show = cv2.resize(frame_show, (160, 160))
                        self.pipe.send(frame_show)

            except Exception as e:
                print("Error:", e)
                break



def run_camera(pipe, stop_event, NS):
    camera = camera_task(NS,pipe,stop_event)
    camera.run()


if __name__ == "__main__":
    print("Camera process started")