import os
from datetime import datetime
from PIL import Image

def get_creation_date(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                date_str = exif_data[36867]

                # Check for the invalid date string
                if date_str == '0000:00:00 00:00:00':
                    return None

                date_object = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                return date_object
    except (AttributeError, KeyError, IndexError, ValueError):
        pass

    # If EXIF data is not available or 36867 is not in exif_data, use file creation time
    return datetime.fromtimestamp(os.path.getctime(file_path))

def organize_photos(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    nodate_folder = os.path.join(destination_folder, "nodate")
    if not os.path.exists(nodate_folder):
        os.makedirs(nodate_folder)

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_path.lower())

            # Skip video files
            if file_extension in {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.3gp', '.m4v'}:
                print(f"Skipped video file: {filename}")
                continue

            creation_date = get_creation_date(file_path)

            if creation_date:
                year_month_folder = os.path.join(destination_folder, creation_date.strftime("%Y-%m"))
                
                if not os.path.exists(year_month_folder):
                    os.makedirs(year_month_folder)
                
                destination_path = os.path.join(year_month_folder, filename)
            else:
                # File does not have date information
                destination_path = os.path.join(nodate_folder, filename)

            # Check if the destination file already exists
            count = 1
            while os.path.exists(destination_path):
                # If the file already exists, append a number to the filename
                base, extension = os.path.splitext(filename)
                new_filename = f"{base}_{count}{extension}"
                destination_path = os.path.join(year_month_folder, new_filename)
                count += 1

            os.rename(file_path, destination_path)
            print(f"Moved {filename} to {destination_path}")

if __name__ == "__main__":
    source_folder = input("Enter the path of the folder containing photos: ")
    destination_folder = input("Enter the path of the destination folder: ")

    organize_photos(source_folder, destination_folder)
