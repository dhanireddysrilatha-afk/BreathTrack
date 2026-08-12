#!/usr/bin/env python3
"""
Photo Organizer
----------------
Scans a folder of photos and sorts them into tidy Year/Month folders,
based on the date each photo was actually taken (read from EXIF data
when available, falling back to the file's last-modified date).

It also renames files to a consistent format:
    YYYY-MM-DD_HHMMSS_originalname.ext

Usage:
    python photo_organizer.py --source ./messy_photos --dest ./organized_photos
    python photo_organizer.py --source ./messy_photos --dest ./organized_photos --dry-run
    python photo_organizer.py --source ./messy_photos --dest ./organized_photos --copy

Author: You! Feel free to customize this.
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS

# File extensions this script will treat as photos
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".tiff", ".bmp", ".gif"}


def get_date_taken(filepath: Path) -> datetime:
    """
    Try to read the 'date taken' from a photo's EXIF metadata.
    If that's not available (e.g. screenshots, PNGs), fall back
    to the file's last-modified timestamp.
    """
    try:
        with Image.open(filepath) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        # Not every image has readable EXIF data — that's fine, we fall back below
        pass

    # Fallback: use the file's last-modified time
    return datetime.fromtimestamp(filepath.stat().st_mtime)


def get_unique_destination(dest_folder: Path, filename: str) -> Path:
    """
    Make sure we never overwrite an existing file. If 'photo.jpg' already
    exists, this returns 'photo_1.jpg', then 'photo_2.jpg', and so on.
    """
    dest_path = dest_folder / filename
    if not dest_path.exists():
        return dest_path

    stem, suffix = dest_path.stem, dest_path.suffix
    counter = 1
    while dest_path.exists():
        dest_path = dest_folder / f"{stem}_{counter}{suffix}"
        counter += 1
    return dest_path


def organize_photos(source: Path, dest: Path, dry_run: bool = False, copy_files: bool = False):
    """
    Walk through the source folder, find photos, and move (or copy)
    them into dest/YYYY/MM/ with a clean, sortable filename.
    """
    if not source.exists():
        print(f"❌ Source folder does not exist: {source}")
        return

    photo_paths = [
        p for p in source.rglob("*")
        if p.is_file() and p.suffix.lower() in PHOTO_EXTENSIONS
    ]

    if not photo_paths:
        print(f"No photos found in {source} (looked for: {', '.join(sorted(PHOTO_EXTENSIONS))})")
        return

    print(f"Found {len(photo_paths)} photo(s) in {source}\n")

    action_word = "Would move" if dry_run else ("Copying" if copy_files else "Moving")
    moved_count = 0

    for photo_path in photo_paths:
        date_taken = get_date_taken(photo_path)

        # Build destination folder: dest/2024/03/
        year_month_folder = dest / f"{date_taken.year:04d}" / f"{date_taken.month:02d}"

        # Build a clean, sortable filename: 2024-03-15_143022_original_name.jpg
        timestamp = date_taken.strftime("%Y-%m-%d_%H%M%S")
        clean_name = f"{timestamp}_{photo_path.name}"

        if dry_run:
            print(f"  {action_word}: {photo_path.name} -> {year_month_folder}/{clean_name}")
        else:
            year_month_folder.mkdir(parents=True, exist_ok=True)
            dest_path = get_unique_destination(year_month_folder, clean_name)

            if copy_files:
                shutil.copy2(photo_path, dest_path)
            else:
                shutil.move(str(photo_path), str(dest_path))

            print(f"  {action_word}: {photo_path.name} -> {dest_path.relative_to(dest)}")

        moved_count += 1

    print(f"\n✅ Done! {moved_count} photo(s) {'would be' if dry_run else ''} organized.")
    if dry_run:
        print("   (This was a dry run — no files were actually touched. Remove --dry-run to apply changes.)")


def main():
    parser = argparse.ArgumentParser(
        description="Sort photos into Year/Month folders based on when they were taken."
    )
    parser.add_argument("--source", required=True, help="Folder containing your messy photos")
    parser.add_argument("--dest", required=True, help="Folder where organized photos will go")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving/copying any files",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of moving them (originals stay in place)",
    )

    args = parser.parse_args()
    organize_photos(
        source=Path(args.source).expanduser().resolve(),
        dest=Path(args.dest).expanduser().resolve(),
        dry_run=args.dry_run,
        copy_files=args.copy,
    )


if __name__ == "__main__":
    main()
