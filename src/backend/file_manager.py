import os
import shutil

def move_file(src_path, dest_folder):
    """
    Moves a file from src_path to dest_folder.
    Creates the destination folder if it doesn't exist.
    """
    try:
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(src_path, dest_folder)
        print(f"Moved file {src_path} to {dest_folder}")
    except Exception as e:
        print(f"Error moving file: {e}")