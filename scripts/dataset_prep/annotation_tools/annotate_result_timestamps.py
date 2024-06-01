
import os
import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
import csv

WIDTH = 640
HEIGHT = 480

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shot-Result Timestamp Annotation")
        self.root.bind('<space>', self.toggle_pause)

        # Video state
        self.paused = True
        self.frame = None
        self.video = None

        # Create GUI elements
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # slider
        self.slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=self.slider_moved)
        self.slider.pack(fill='x', expand=True)
        self.slider_last = 0

        # Buttons
        load_button = tk.Button(root, text="Load Video", command=self.load_video)
        load_button.pack(side=tk.LEFT)

        self.batch_fps = []

        play_button = tk.Button(root, text="Play/Pause", command=self.toggle_pause)
        play_button.pack(side=tk.LEFT)

        annotate_button = tk.Button(root, text="Annotate", command=self.annotate)
        annotate_button.pack(side=tk.LEFT)

        # CSV setup
        self.csv_file_path = 'annotations.csv'

        with open(self.csv_file_path, 'w', newline='') as cv:
            csv_writer = csv.writer(cv, delimiter=',')
            csv_writer.writerow(['video_path', 'frame_index'])  # CSV header

        self.annotation_count = 0
        self.label = tk.Label(root, text=f"Annotations: {self.annotation_count}")
        self.label.pack()
    
    def annotate(self):
        if self.video and self.video.isOpened():
            frame_number = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            video_path = self.batch_fps[-1]

            # see if this works 
            with open(self.csv_file_path, 'a', newline='') as cv:
                csv_writer = csv.writer(cv, delimiter=',')
                csv_writer.writerow([video_path, frame_number])

            self.annotation_count += 1
            self.label.config(text=f"Annotations: {self.annotation_count}")
            print(f"Annotation added: {video_path}, Frame: {frame_number}")

            self.batch_fps.pop(-1)
            self.load_video()

    def load_batch(self, directory):
        video_formats = ('.mp4', '.avi', '.mov', '.mkv')
        # Walk through all directories and files in 'directory'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(video_formats):
                    full_path = os.path.join(root, file)
                    self.batch_fps.append(full_path)
        print(f"Loaded {len(self.batch_fps)} videos.")

    def slider_moved(self, val):
        if self.video:
            frame_number = int(float(val))
            if abs(frame_number - self.slider_last) > 2:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                self.slider_last = frame_number
                
                # display the current frame
                ret, frame = self.video.read()
                if ret:
                    self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frame = cv2.resize(self.frame, (WIDTH, HEIGHT)) 
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                    self.canvas.update()

    def load_video(self):
        fp = self.batch_fps[-1]
        if fp:
            self.video = cv2.VideoCapture(fp)
            self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider.configure(to=self.length - 1)
            self.paused = False

            # pop fp off end of vid
            self.play_video()

    def play_video(self):
        def stream():
            while not self.paused:
                if self.video.isOpened():
                    self.slider_last = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                    self.slider.set(self.slider_last)
                    ret, frame = self.video.read()
                    if ret:
                        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        self.frame = cv2.resize(self.frame, (WIDTH, HEIGHT)) 
                        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                        self.canvas.update()
                    else:
                        self.paused = True
                        break

        threading.Thread(target=stream).start()

    def toggle_pause(self, event=None):
        if self.paused:
            self.paused = False
            self.play_video()
        else:
            self.paused = True

    def on_closing(self):
        self.paused = True
        self.root.destroy()

if __name__ == '__main__':

    root = tk.Tk()
    player = VideoPlayer(root)
    root.protocol("WM_DELETE_WINDOW", player.on_closing)
    player.load_batch('/Users/leviharris/Desktop/shot_attempts_xy_nba_1k')

    root.after(0, player.load_video)
    root.mainloop()