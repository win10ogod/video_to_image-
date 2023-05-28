import cv2
from tqdm import tqdm
import argparse
import os

def extract_frames(video_path, output_dir):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize progress bar
    pbar = tqdm(total=total_frames, unit='frames', desc='Extracting frames')
    
    # Extract frames
    frame_count = 0
    while True:
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract frames from a video')
    parser.add_argument('video_path', help='absolute path to the video file')
    parser.add_argument('output_dir', help='absolute path to the directory to save the extracted frames')
    args = parser.parse_args()
    
    # Extract frames from the video
    extract_frames(args.video_path, args.output_dir)
