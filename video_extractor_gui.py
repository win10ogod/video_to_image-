import cv2
from tqdm import tqdm
import argparse
import os
import tkinter as tk
from tkinter import filedialog

class VideoExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.video_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.start_time = tk.DoubleVar()
        self.end_time = tk.DoubleVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Video Path Entry
        video_label = tk.Label(self.root, text='Video File:')
        video_label.grid(row=0, column=0)
        video_entry = tk.Entry(self.root, textvariable=self.video_path, width=50)
        video_entry.grid(row=0, column=1)
        video_browse_btn = tk.Button(self.root, text='Browse', command=self.browse_video)
        video_browse_btn.grid(row=0, column=2)
        
        # Output Directory Entry
        output_label = tk.Label(self.root, text='Output Directory:')
        output_label.grid(row=1, column=0)
        output_entry = tk.Entry(self.root, textvariable=self.output_dir, width=50)
        output_entry.grid(row=1, column=1)
        output_browse_btn = tk.Button(self.root, text='Browse', command=self.browse_output_dir)
        output_browse_btn.grid(row=1, column=2)
        
        # Start Time Entry
        start_label = tk.Label(self.root, text='Start Time (seconds):')
        start_label.grid(row=2, column=0)
        start_entry = tk.Entry(self.root, textvariable=self.start_time)
        start_entry.grid(row=2, column=1)
        
        # End Time Entry
        end_label = tk.Label(self.root, text='End Time (seconds):')
        end_label.grid(row=3, column=0)
        end_entry = tk.Entry(self.root, textvariable=self.end_time)
        end_entry.grid(row=3, column=1)
        
        # Extract Button
        extract_btn = tk.Button(self.root, text='Extract Frames', command=self.extract_frames)
        extract_btn.grid(row=4, column=1)
        
    def browse_video(self):
        video_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4;*.avi')])
        self.video_path.set(video_path)
    
    def browse_output_dir(self):
        output_dir = filedialog.askdirectory()
        self.output_dir.set(output_dir)
    
    def extract_frames(self):
        video_path = self.video_path.get()
        output_dir = self.output_dir.get()
        start_time = self.start_time.get()
        end_time = self.end_time.get()
        
        if not video_path or not output_dir:
            return
        
        # Open the video file
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Convert time to frame indices
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        if start_frame >= total_frames:
            print("Start time exceeds video duration.")
            return
        if end_frame >= total_frames:
            end_frame = total_frames - 1
        
        # Set the starting frame
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize progress bar
        frames_to_extract = end_frame - start_frame + 1
        pbar = tqdm(total=frames_to_extract, unit='frames', desc='Extracting frames')
        
        # Extract frames
        frame_count = 0
        while frame_count <= end_frame:
            # Read the next frame
            ret, frame = video.read()
            if not ret:
                break
            
            # Save the frame as an image
            frame_path = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_path, frame)
            
            # Update progress bar
            frame_count += 1
            pbar.update(1)
        
        # Release the video file and close the progress bar
        video.release()
        pbar.close()

if __name__ == '__main__':
    # Create the Tkinter application window
    root = tk.Tk()
    root.title('Video Extractor')
    
    # Create the VideoExtractorGUI instance
    app = VideoExtractorGUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()
