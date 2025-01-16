import os
from datetime import datetime
from moviepy.editor import VideoFileClip
import shutil
import subprocess

def get_media_created_date(file_path):
    _, file_extension = os.path.splitext(file_path.lower())

    # Include MP4 and MOV files
    if file_extension not in {'.mp4', '.mov'}:
        return None

    try:
        # Use ffprobe to get media created date
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream_tags=creation_time', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        creation_time_str = subprocess.check_output(ffprobe_cmd, universal_newlines=True).strip()

        if creation_time_str:
            creation_date = datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            return creation_date
    except Exception as e:
        print(f"Error processing video file {file_path}: {e}")
    return None

def organize_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            creation_date = get_media_created_date(file_path)
            
            if creation_date:
                year_month_folder = os.path.join(destination_folder, creation_date.strftime("%Y-%m"))
                
                if not os.path.exists(year_month_folder):
                    os.makedirs(year_month_folder)
                
                destination_path = os.path.join(year_month_folder, filename)

                # Check if the destination file already exists
                count = 1
                while os.path.exists(destination_path):
                    # If the file already exists, append a number to the filename
                    base, extension = os.path.splitext(filename)
                    new_filename = f"{base}_{count}{extension}"
                    destination_path = os.path.join(year_month_folder, new_filename)
                    count += 1
                
                try:
                    shutil.copy(file_path, destination_path)
                    os.remove(file_path)
                    print(f"Moved {filename} to {destination_path}")
                except PermissionError:
                    print(f"Skipped {filename} due to ongoing access by another process")

if __name__ == "__main__":
    source_folder = input("Enter the path of the folder containing files: ")
    destination_folder = input("Enter the path of the destination folder: ")

    organize_files(source_folder, destination_folder)
