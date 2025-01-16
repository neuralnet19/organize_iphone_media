import os
from datetime import datetime
import shutil

def get_media_modified_date(file_path):
    _, file_extension = os.path.splitext(file_path.lower())

    # Include only MP4 files
    if file_extension != '.mp4':
        return None

    try:
        modified_time = os.path.getmtime(file_path)
        modification_date = datetime.fromtimestamp(modified_time)
        return modification_date
    except Exception as e:
        print(f"Error processing MP4 file {file_path}: {e}")
    return None

def organize_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            modification_date = get_media_modified_date(file_path)
            
            if modification_date:
                year_month_folder = os.path.join(destination_folder, modification_date.strftime("%Y-%m"))
                
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
    source_folder = input("Enter the path of the folder containing MP4 files: ")
    destination_folder = input("Enter the path of the destination folder: ")

    organize_files(source_folder, destination_folder)
