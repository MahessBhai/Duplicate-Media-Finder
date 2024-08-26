import os
import cv2
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def show_image(image_path):
    try:
        image = Image.open(image_path)
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Error displaying image {image_path}: {e}")

def show_video(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
        video.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error displaying video {video_path}: {e}")

def process_duplicates(duplicates_file):
    df = pd.read_excel(duplicates_file)
    
    for _, row in df.iterrows():
        original_file = row['Original File']
        duplicate_file = row['Duplicate File']

        print(f"Displaying original file: {original_file}")
        if original_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            show_image(original_file)
        elif original_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            show_video(original_file)
        
        print(f"Displaying duplicate file: {duplicate_file}")
        if duplicate_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            show_image(duplicate_file)
        elif duplicate_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            show_video(duplicate_file)
        
        confirm = input(f"Do you want to delete the duplicate file {duplicate_file}? (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                os.remove(duplicate_file)
                print(f"Deleted {duplicate_file}.")
            except Exception as e:
                print(f"Error deleting file {duplicate_file}: {e}")
        else:
            print(f"Skipped deleting {duplicate_file}.")

if __name__ == "__main__":
    duplicates_file = "duplicates.xlsx"  # Path to the Excel file with duplicates
    process_duplicates(duplicates_file)
