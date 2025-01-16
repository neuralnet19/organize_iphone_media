import os
from datetime import datetime
import shutil
from PIL import Image, ExifTags

def get_date_taken(file_path):
    """
    Extracts the 'DateTimeOriginal' metadata from the image file using PIL.
    Falls back to the file's modification time if metadata is unavailable.
    """
    try:
        # Open the image file
        with Image.open(file_path) as img:
            # Extract EXIF data
            exif_data = img._getexif()

            if exif_data:
                # Search for DateTimeOriginal in EXIF tags
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id)
                    if tag_name == "DateTimeOriginal":
                        # Convert to datetime object
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        # Log any issues (optional)
        print(f"Metadata extraction failed for {file_path}: {e}")

    # Default to file modification time if metadata is missing
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def organize_photos(source_folder, destination_folder):
    """
    Organizes photos from source_folder into year-month subfolders in destination_folder,
    sorted by the date taken. Files without metadata are placed in a 'nodate' folder.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    nodate_folder = os.path.join(destination_folder, "nodate")
    if not os.path.exists(nodate_folder):
        os.makedirs(nodate_folder)

    processed_files = 0

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_path.lower())

            # Skip video files
            if file_extension in {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.3gp', '.m4v'}:
                print(f"Skipped video file: {filename}")
                continue

            # Get the date taken
            date_taken = get_date_taken(file_path)

            if date_taken:
                # Create folder path based on year-month of date taken
                year_month_folder = os.path.join(destination_folder, date_taken.strftime("%Y-%m"))
                if not os.path.exists(year_month_folder):
                    os.makedirs(year_month_folder)

                destination_path = os.path.join(year_month_folder, filename)
            else:
                # No date information, use 'nodate' folder
                destination_path = os.path.join(nodate_folder, filename)

            # Handle duplicate file names
            count = 1
            original_path = destination_path
            while os.path.exists(destination_path):
                base, extension = os.path.splitext(original_path)
                destination_path = f"{base}_{count}{extension}"
                count += 1

            try:
                # Copy file to the destination
                shutil.copy(file_path, destination_path)
                processed_files += 1
                print(f"Copied {filename} to {destination_path}")
            except PermissionError as e:
                print(f"Error: Could not copy {filename}. File might be in use or locked. {e}")

    print(f"Processed {processed_files} files.")

if __name__ == "__main__":
    source_folder = input("Enter the path of the folder containing photos: ").strip()
    destination_folder = input("Enter the path of the destination folder: ").strip()

    organize_photos(source_folder, destination_folder)
