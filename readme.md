# Photo and Video Organizer Scripts

A collection of Python scripts to automatically organize photos and videos into folders by date. These scripts sort media files into year-month folders based on their creation dates, making it easier to manage large collections of photos and videos.

## Features

- Organizes photos and videos into folders structured by year and month (e.g., "2024-01")
- Handles duplicate filenames by appending numbers
- Supports multiple file formats:
  - Photos: Standard image formats including HEIC
  - Videos: MP4 and MOV files
- Extracts creation dates from:
  - EXIF metadata for photos
  - Media creation time for videos
  - File modification time as fallback
- Creates a special "nodate" folder for files without valid date information

## Scripts

1. `organize_videos_mov.py`: Organizes MP4 and MOV video files using media creation time
2. `organize_videos_mp4.py`: Organizes MP4 files using file modification time
3. `organize_photos_heic.py`: Organizes photos including HEIC format using EXIF data
4. `organize_photos.py`: Organizes standard photo formats using EXIF data

## Requirements

- Python 3.x
- Required Python packages:
  ```
  Pillow
  moviepy
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/photo-organizer.git
   ```

2. Install required packages:
   ```bash
   pip install Pillow moviepy
   ```

## Usage

Each script can be run independently depending on your needs:

1. Run the desired script:
   ```bash
   python organize_photos.py
   # or
   python organize_videos_mov.py
   # etc.
   ```

2. When prompted, enter:
   - The source folder path containing your media files
   - The destination folder path where you want the organized folders to be created

## Output Structure

```
destination_folder/
├── 2024-01/
│   ├── photo1.jpg
│   ├── video1.mp4
│   └── ...
├── 2024-02/
│   ├── photo2.jpg
│   ├── video2.mov
│   └── ...
└── nodate/
    └── files_with_no_date_info.*
```

## Notes

- Scripts will create the destination folder structure if it doesn't exist
- Duplicate filenames are handled by appending a number (e.g., `photo_1.jpg`)
- Files that are currently in use or locked will be skipped with a notification
- Video organization requires ffprobe for the MOV/MP4 script

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

None

---

<p align="center">
  <img src="https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif" alt="Code is Life" width="120">
</p>

<p align="center">
  <b>⌨️ with 💻 by Raj Reddy</b><br>
  <code>// Reach out if you find bugs in the matrix</code><br>
  <a href="https://github.com/neuralnet19" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-000000?style=flat-square&logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="mailto:neuralnet19@hotmail.com" target="_blank">
    <img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email">
  </a>
</p>

<p align="center">
  <code>// "Hello, World!" is just the beginning 🚀</code>
</p>

---
