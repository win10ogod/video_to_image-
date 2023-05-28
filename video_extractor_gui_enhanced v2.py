import cv2
from tqdm import tqdm
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


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
        
        # Extract Frames Button
        extract_frames_btn = tk.Button(self.root, text='Extract Frames', command=self.extract_frames)
        extract_frames_btn.grid(row=4, column=1)
        
        # Extract Audio Button
        extract_audio_btn = tk.Button(self.root, text='Extract Audio', command=self.extract_audio)
        extract_audio_btn.grid(row=5, column=1)
        
        # Compose Video Button
        compose_video_btn = tk.Button(self.root, text='Compose Video', command=self.compose_video)
        compose_video_btn.grid(row=6, column=1)
        
        # Combine Video and Audio Button
        combine_btn = tk.Button(self.root, text='Combine Video and Audio', command=self.combine_video_audio)
        combine_btn.grid(row=7, column=1)
        
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
        
        # Show completion message
        messagebox.showinfo('Extraction Complete', f'Frames extracted: {frame_count}')
    
    def extract_audio(self):
        video_path = self.video_path.get()
        output_dir = self.output_dir.get()
        
        if not video_path or not output_dir:
            messagebox.showerror('Error', 'Video file path and output directory are required.')
            return
        
        # Check if video file exists
        if not os.path.isfile(video_path):
            messagebox.showerror('Error', 'Video file does not exist.')
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract audio using moviepy
        video = VideoFileClip(video_path)
        audio_path = os.path.join(output_dir, 'audio.wav')
        video.audio.write_audiofile(audio_path)
        video.close()
        
        # Show completion message
        messagebox.showinfo('Extraction Complete', 'Audio extracted successfully.')
    
    def compose_video(self):
        video_path = self.video_path.get()
        frame_dir = self.output_dir.get()
        
        if not video_path or not frame_dir:
            messagebox.showerror('Error', 'Video file path and frame directory are required.')
            return
        
        # Check if video file exists
        if not os.path.isfile(video_path):
            messagebox.showerror('Error', 'Video file does not exist.')
            return
        
        # Create frame directory if it doesn't exist
        os.makedirs(frame_dir, exist_ok=True)
        
        # Get video properties
        fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)
        
        # Get sorted list of frame files
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.startswith('frame_')])
        
        if not frame_files:
            messagebox.showerror('Error', 'No frame images found in the specified directory.')
            return
        
        # Create video writer
        video_writer = cv2.VideoWriter(os.path.join(frame_dir, 'composed_video.mp4'),
                                       cv2.VideoWriter_fourcc(*'mp4v'), fps, (1920, 1080))
        
        # Compose video frame by frame
        for frame_file in frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame = cv2.imread(frame_path)
            video_writer.write(frame)
        
        # Release the video writer
        video_writer.release()
        
        # Show completion message
        messagebox.showinfo('Composition Complete', 'Video composed successfully.')
    
    def combine_video_audio(self):
        video_path = self.video_path.get()
        frame_dir = self.output_dir.get()
        
        if not video_path or not frame_dir:
            messagebox.showerror('Error', 'Video file path and frame directory are required.')
            return
        
        # Check if video file exists
        if not os.path.isfile(video_path):
            messagebox.showerror('Error', 'Video file does not exist.')
            return
        
        # Check if frame directory exists
        if not os.path.isdir(frame_dir):
            messagebox.showerror('Error', 'Frame directory does not exist.')
            return
        
        # Get video properties
        fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)
        
        # Get sorted list of frame files
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.startswith('frame_')])
        
        if not frame_files:
            messagebox.showerror('Error', 'No frame images found in the specified directory.')
            return
        
        # Create video writer
        video_writer = cv2.VideoWriter(os.path.join(frame_dir, 'combined_video.mp4'),
                                       cv2.VideoWriter_fourcc(*'mp4v'), fps, (1920, 1080))
        
        # Compose video frame by frame
        for frame_file in frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame = cv2.imread(frame_path)
            video_writer.write(frame)
        
        # Release the video writer
        video_writer.release()
        
        # Get audio file path
        audio_path = os.path.join(frame_dir, 'audio.wav')
        
        # Combine video and audio using moviepy
        video = VideoFileClip(os.path.join(frame_dir, 'combined_video.mp4'))
        audio = AudioSegment.from_wav(audio_path)
        
        # Check if audio duration matches video duration
        if audio.duration_seconds != video.duration:
            messagebox.showerror('Error', 'Audio and video durations do not match.')
            return
        
        video = video.set_audio(audio)
        video.write_videofile(os.path.join(frame_dir, 'final_video.mp4'), codec='libx264')
        
        # Show completion message
        messagebox.showinfo('Combination Complete', 'Video and audio combined successfully.')


if __name__ == '__main__':
    # Create the Tkinter application window
    root = tk.Tk()
    root.title('Video Extractor')
    
    # Create the VideoExtractorGUI instance
    app = VideoExtractorGUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()

