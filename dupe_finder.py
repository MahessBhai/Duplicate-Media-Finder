import os
import hashlib
import json
import pandas as pd
from PIL import Image
import imagehash
import cv2

def hash_file(filepath):
    with open(filepath, 'rb') as f:
        hasher = hashlib.md5()
        buffer = f.read(65536)  # Read file in chunks
        while buffer:
            hasher.update(buffer)
            buffer = f.read(65536)
        return hasher.hexdigest()

def hash_image(filepath):
    try:
        image = Image.open(filepath)
        return str(imagehash.phash(image))  # Perceptual hash
    except Exception as e:
        print(f"Error hashing image {filepath}: {e}")
        return None

def hash_video(filepath):
    """Generate a hash for a video based on its keyframes."""
    try:
        video = cv2.VideoCapture(filepath)
        success, frame = video.read()
        processed_hashes = set()
        video_hashes = []
        no_unique_frames_count = 0  # Track the number of consecutive iterations with no unique frame
        no_unique_frames_limit = 20  # Limit after which to break the loop
        
        while success:
            frame_hash = hashlib.md5(cv2.imencode('.jpg', frame)[1].tobytes()).hexdigest()
            if frame_hash not in processed_hashes:
                video_hashes.append(frame_hash)
                processed_hashes.add(frame_hash)
                no_unique_frames_count = 0  # Reset the count since we found a unique frame
            else:
                no_unique_frames_count += 1
            # Break if too many iterations with no new unique frame
            if no_unique_frames_count > no_unique_frames_limit:
                print("Breaking loop due to too many repeated frames.")
                break
            # Skip some frames to reduce processing time
            video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) + 30)
            success, frame = video.read()
        video.release()
        if video_hashes:
            # Combine all unique frame hashes into a single hash
            return hashlib.md5(''.join(video_hashes).encode()).hexdigest()
        else:
            return None
    except Exception as e:
        print(f"Error hashing video {filepath}: {e}")
        return None
    
def load_checksums(checksum_file):
    if os.path.exists(checksum_file):
        with open(checksum_file, 'r') as f:
            return json.load(f)
    return {}

def save_checksums(checksum_file, checksums):
    with open(checksum_file, 'w') as f:
        json.dump(checksums, f, indent=4)

def find_duplicates(directory, checksum_file='checksums.json', export_file='duplicates.xlsx'):
    checksums = load_checksums(checksum_file)
    duplicates = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            print(f'doing file {filename} right now')
            filepath = os.path.join(dirpath, filename)
            extension = os.path.splitext(filepath)[1].lower()

            if extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                file_hash = hash_image(filepath)
            elif extension in ['.mp4', '.avi', '.mov', '.mkv']:
                file_hash = hash_video(filepath)
            else:
                file_hash = hash_file(filepath)

            if file_hash:
                if file_hash in checksums:
                    original_path = checksums[file_hash]
                    if original_path != filepath:
                        duplicates.append((original_path, filepath))
                else:
                    checksums[file_hash] = filepath
    save_checksums(checksum_file, checksums)
    
    if duplicates:
        df = pd.DataFrame(duplicates, columns=['Original File', 'Duplicate File'])
        df.to_excel(export_file, index=False)
        print(f"Duplicate file paths exported to {export_file}.")
    else:
        print("No duplicates found.")
    
    return duplicates

if __name__ == "__main__":
    directory = {path_to_directory}
    duplicates = find_duplicates(directory)
