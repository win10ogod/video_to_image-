import cv2
from tqdm import tqdm
import argparse
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class VideoExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.video_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.start_time = tk.DoubleVar()
        self.end_time = tk.DoubleVar()
        self.acceleration_var = tk.StringVar(value='CPU')
        
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
        
        # Acceleration Option
        acceleration_label = tk.Label(self.root, text='Acceleration:')
        acceleration_label.grid(row=4, column=0)
        acceleration_option = tk.OptionMenu(self.root, self.acceleration_var, 'CPU', 'GPU')
        acceleration_option.grid(row=4, column=1)
        
        # Extract Button
        extract_btn = tk.Button(self.root, text='Extract Frames', command=self.extract_frames)
        extract_btn.grid(row=5, column=1)
        
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
        acceleration = self.acceleration_var.get()
        
        if not video_path or not output_dir:
            messagebox.showerror('Error', 'Video file path and output directory are required.')
            return
        
        # Check if video file exists
        if not os.path.isfile(video_path):
            messagebox.showerror('Error', 'Video file does not exist.')
            return
        
        # Open the video file
        video = cv2.VideoCapture(video_path)
        
        # Check if video is successfully opened
        if not video.isOpened():
            messagebox.showerror('Error', 'Failed to open video file.')
            return
        
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Convert time to frame indices
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        if start_frame >= total_frames:
            messagebox.showerror('Error', 'Start time exceeds video duration.')
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
        
        # Select acceleration device
        if acceleration == 'GPU':
            if cv2.cuda.getCudaEnabledDeviceCount() == 0:
                messagebox.showwarning('Warning', 'No GPU device available. Switching to CPU acceleration.')
                acceleration = 'CPU'
            else:
                video.set(cv2.CAP_PROP_CUDA_DEVICE, 0)
        
        # Create video writer for GPU acceleration
        if acceleration == 'GPU':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter()
            success = video_writer.open(os.path.join(output_dir, 'preview.mp4'), fourcc, fps, (1920, 1080), True)
        
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
            
            # Show preview for CPU acceleration
            if acceleration == 'CPU':
                cv2.imshow('Preview', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            
            # Write frame to video for GPU acceleration
            if acceleration == 'GPU':
                video_writer.write(frame)
            
            # Update progress bar
            frame_count += 1
            pbar.update(1)
        
        # Release the video file, close the progress bar, and destroy preview window
        video.release()
        pbar.close()
        cv2.destroyAllWindows()
        
        # Show completion message
        messagebox.showinfo('Extraction Complete', f'Frames extracted: {frame_count}')

if __name__ == '__main__':
    # Create the Tkinter application window
    root = tk.Tk()
    root.title('Video Extractor')
    
    # Create the VideoExtractorGUI instance
    app = VideoExtractorGUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()
