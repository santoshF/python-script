#!/usr/bin/env python3
"""
rename_files.py - Automate file renaming in a folder
Usage: python3 rename_files.py [options]
"""

import os
import sys
import argparse
import re
import shutil
import fnmatch
from pathlib import Path


def rename_sequential(folder_path, prefix="file", extension=None, dry_run=True):
    """Rename files sequentially (file_1, file_2, etc.)"""
    try:
        files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        if not files:
            print("No files found in the folder.")
            return
        
        for index, filename in enumerate(files, 1):
            old_path = os.path.join(folder_path, filename)
            
            if extension:
                new_filename = f"{prefix}_{index}{extension}"
            else:
                file_ext = os.path.splitext(filename)[1]
                new_filename = f"{prefix}_{index}{file_ext}"
            
            new_path = os.path.join(folder_path, new_filename)
            
            if dry_run:
                print(f"[DRY RUN] {filename} → {new_filename}")
            else:
                os.rename(old_path, new_path)
                print(f"✓ {filename} → {new_filename}")
    
    except Exception as e:
        print(f"Error: {e}")


def rename_replace(folder_path, search_text, replace_text, dry_run=True):
    """Replace text in filenames"""
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print("No files found in the folder.")
            return
        
        count = 0
        for filename in files:
            if search_text in filename:
                new_filename = filename.replace(search_text, replace_text)
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                
                if dry_run:
                    print(f"[DRY RUN] {filename} → {new_filename}")
                else:
                    os.rename(old_path, new_path)
                    print(f"✓ {filename} → {new_filename}")
                count += 1
        
        if count == 0:
            print(f"No files found containing '{search_text}'")
    
    except Exception as e:
        print(f"Error: {e}")


def rename_regex(folder_path, pattern, replacement, dry_run=True):
    """Rename files using regex pattern"""
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print("No files found in the folder.")
            return
        
        count = 0
        for filename in files:
            new_filename = re.sub(pattern, replacement, filename)
            if new_filename != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                
                if dry_run:
                    print(f"[DRY RUN] {filename} → {new_filename}")
                else:
                    os.rename(old_path, new_path)
                    print(f"✓ {filename} → {new_filename}")
                count += 1
        
        if count == 0:
            print(f"No files matched the pattern '{pattern}'")
    
    except Exception as e:
        print(f"Error: {e}")


def rename_lowercase(folder_path, dry_run=True):
    """Convert filenames to lowercase"""
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print("No files found in the folder.")
            return
        
        count = 0
        for filename in files:
            new_filename = filename.lower()
            if new_filename != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                
                if dry_run:
                    print(f"[DRY RUN] {filename} → {new_filename}")
                else:
                    os.rename(old_path, new_path)
                    print(f"✓ {filename} → {new_filename}")
                count += 1
        
        if count == 0:
            print("No files needed renaming to lowercase")
    
    except Exception as e:
        print(f"Error: {e}")


def rename_remove_spaces(folder_path, separator="_", dry_run=True):
    """Remove spaces from filenames"""
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print("No files found in the folder.")
            return
        
        count = 0
        for filename in files:
            new_filename = filename.replace(" ", separator)
            if new_filename != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)
                
                if dry_run:
                    print(f"[DRY RUN] {filename} → {new_filename}")
                else:
                    os.rename(old_path, new_path)
                    print(f"✓ {filename} → {new_filename}")
                count += 1
        
        if count == 0:
            print("No files with spaces found")
    
    except Exception as e:
        print(f"Error: {e}")


def move_files(src_folder, dst_folder, pattern=None, dry_run=True):
    """Move files from src_folder to dst_folder, optionally filtered by a glob pattern."""
    try:
        files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
        if not files:
            print("No files found in the source folder.")
            return

        if pattern:
            files = [f for f in files if fnmatch.fnmatch(f, pattern)]
            if not files:
                print(f"No files matched the pattern '{pattern}'")
                return

        if not os.path.isdir(dst_folder):
            if dry_run:
                print(f"[DRY RUN] Would create directory: {dst_folder}")
            else:
                os.makedirs(dst_folder, exist_ok=True)
                print(f"Created directory: {dst_folder}")

        moved = 0
        skipped = 0
        for filename in files:
            src_path = os.path.join(src_folder, filename)
            dst_path = os.path.join(dst_folder, filename)

            if os.path.exists(dst_path):
                print(f"[SKIPPED] {filename} — already exists in destination")
                skipped += 1
                continue

            if dry_run:
                print(f"[DRY RUN] {src_path} → {dst_path}")
            else:
                shutil.move(src_path, dst_path)
                print(f"✓ {filename} → {dst_folder}")
            moved += 1

        summary = f"{moved} file(s) {'would be ' if dry_run else ''}moved"
        if skipped:
            summary += f", {skipped} skipped (collision)"
        print(f"\n{summary}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Automate file renaming in a folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sequential rename (dry run)
  python3 rename_files.py -d ~/Documents --sequential -p "photo"
  
  # Sequential rename (execute)
  python3 rename_files.py -d ~/Documents --sequential -p "photo" --execute
  
  # Replace text in filenames
  python3 rename_files.py -d ~/Documents --replace "old" "new" --execute
  
  # Convert to lowercase
  python3 rename_files.py -d ~/Documents --lowercase --execute
  
  # Remove spaces from filenames
  python3 rename_files.py -d ~/Documents --remove-spaces --execute
  
  # Use regex pattern
  python3 rename_files.py -d ~/Documents --regex "(\d+)" "photo_\\1" --execute

  # Move all files to another directory (dry run)
  python3 rename_files.py -d ~/Downloads --move --dest ~/Archive

  # Move only JPEGs and execute
  python3 rename_files.py -d ~/Downloads --move --dest ~/Photos --pattern "*.jpg" --execute
        """
    )
    
    parser.add_argument(
        "-d", "--directory",
        type=str,
        default=".",
        help="Directory path containing files to rename (default: current directory)"
    )
    
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Rename files sequentially"
    )
    
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default="file",
        help="Prefix for sequential renaming (default: 'file')"
    )
    
    parser.add_argument(
        "-e", "--extension",
        type=str,
        help="Force file extension (e.g., '.jpg')"
    )
    
    parser.add_argument(
        "--replace",
        nargs=2,
        metavar=("SEARCH", "REPLACE"),
        help="Replace text in filenames"
    )
    
    parser.add_argument(
        "--regex",
        nargs=2,
        metavar=("PATTERN", "REPLACEMENT"),
        help="Rename using regex pattern"
    )
    
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Convert filenames to lowercase"
    )
    
    parser.add_argument(
        "--remove-spaces",
        action="store_true",
        help="Replace spaces with underscores"
    )
    
    parser.add_argument(
        "-s", "--separator",
        type=str,
        default="_",
        help="Separator for remove-spaces option (default: '_')"
    )
    
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files to another directory"
    )

    parser.add_argument(
        "--dest",
        type=str,
        metavar="DESTINATION",
        help="Destination directory for --move"
    )

    parser.add_argument(
        "--pattern",
        type=str,
        metavar="GLOB",
        help="Glob pattern to filter files for --move (e.g. '*.jpg')"
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute renaming (without this flag, shows dry run only)"
    )
    
    args = parser.parse_args()
    
    # Expand user path
    folder_path = os.path.expanduser(args.directory)
    
    # Validate folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Directory '{folder_path}' not found")
        sys.exit(1)
    
    print(f"Directory: {folder_path}")
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")
    print("-" * 50)
    
    # Execute selected operation
    if args.sequential:
        rename_sequential(folder_path, args.prefix, args.extension, dry_run=not args.execute)
    elif args.replace:
        rename_replace(folder_path, args.replace[0], args.replace[1], dry_run=not args.execute)
    elif args.regex:
        rename_regex(folder_path, args.regex[0], args.regex[1], dry_run=not args.execute)
    elif args.lowercase:
        rename_lowercase(folder_path, dry_run=not args.execute)
    elif args.remove_spaces:
        rename_remove_spaces(folder_path, args.separator, dry_run=not args.execute)
    elif args.move:
        if not args.dest:
            parser.error("--move requires --dest <destination>")
        dest_path = os.path.expanduser(args.dest)
        move_files(folder_path, dest_path, args.pattern, dry_run=not args.execute)
    else:
        parser.print_help()
        sys.exit(1)
    
    print("-" * 50)
    if not args.execute:
        print("\n✓ This was a DRY RUN. Add --execute flag to apply changes.")


if __name__ == "__main__":
    main()
