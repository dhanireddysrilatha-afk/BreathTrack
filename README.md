<<<<<<< HEAD
# 📸 Photo Organizer

A simple Python script that automatically sorts a messy folder of photos into
clean `Year/Month` folders, based on when each photo was actually taken.

No more scrolling through thousands of unsorted photos — run this once and
your photo collection becomes organized and easy to browse.

## What it does

- Scans a folder (and subfolders) for photos
- Reads the **date taken** from each photo's metadata (EXIF), falling back
  to the file's last-modified date if no metadata is available
- Sorts photos into `destination/YYYY/MM/` folders
- Renames files to a clean, sortable format: `2024-03-15_143022_original_name.jpg`
- Never overwrites files — automatically handles naming collisions
- Supports a `--dry-run` mode so you can preview changes safely before applying them
- Supports `--copy` mode if you want to keep your originals untouched

## Example

**Before:**
```
messy_photos/
├── IMG_2043.jpg
├── vacation_pic.png
├── screenshot.png
└── beach_day.jpg
```

**After:**
```
organized_photos/
├── 2023/
│   ├── 06/
│   │   └── 2023-06-12_091533_IMG_2043.jpg
│   └── 08/
│       └── 2023-08-02_142201_beach_day.jpg
└── 2024/
    └── 01/
        └── 2024-01-15_103045_vacation_pic.png
```

## Installation

1. Make sure you have Python 3.8+ installed.
2. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/photo-organizer.git
   cd photo-organizer
   ```
3. Install the one dependency (Pillow, for reading photo metadata):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**Preview what will happen (recommended first step):**
```bash
python photo_organizer.py --source ./messy_photos --dest ./organized_photos --dry-run
```

**Actually organize your photos (moves files):**
```bash
python photo_organizer.py --source ./messy_photos --dest ./organized_photos
```

**Organize but keep your originals in place (copies instead of moves):**
```bash
python photo_organizer.py --source ./messy_photos --dest ./organized_photos --copy
```

### Options

| Flag | Description |
|------|-------------|
| `--source` | Path to the folder containing your unsorted photos (required) |
| `--dest` | Path to the folder where organized photos will be placed (required) |
| `--dry-run` | Preview changes without touching any files |
| `--copy` | Copy files instead of moving them |

## Supported file types

`.jpg` `.jpeg` `.png` `.heic` `.tiff` `.bmp` `.gif`

## How it works

The script uses [Pillow](https://python-pillow.org/) to read each photo's
EXIF metadata and pull out the `DateTimeOriginal` tag — the timestamp your
camera or phone embeds in the file when the photo was taken. If a photo has
no EXIF data (common for screenshots or downloaded images), it falls back to
the file's last-modified timestamp on disk.

## Ideas for extending this project

- Detect and skip exact duplicate photos (by file hash)
- Add support for videos (`.mp4`, `.mov`) using their creation date
- Add a `--by-day` option for finer-grained folders
- Build a simple GUI with `tkinter`
- Add a progress bar for large photo libraries

## License

MIT — feel free to use, modify, and share.
=======
# BreathTrack
A simple tool to help people monitor their breathing patterns and respiratory health over time. Users can log symptoms, breathing exercises, and peak flow readings, then view trends to spot changes that might be worth discussing with a doctor.
>>>>>>> 886a45a962b47505fb8ec3cf47a8bfd2fa8b2562
