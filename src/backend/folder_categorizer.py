import os
import shutil

# Helper function to move multiple files to the appropriate category folder
def move_files_to_category_folder(file_paths, dest_folder):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create the directory if it doesn't exist

    for src_path in file_paths:
        try:
            # Ensure the source file exists before trying to move it
            if not os.path.exists(src_path):
                print(f"Source file not found: {src_path}")
                continue

            filename = os.path.basename(src_path)
            dest_path = os.path.join(dest_folder, filename)

            # Check if file already exists in destination and append a number if so
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                new_dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                while os.path.exists(new_dest_path):
                    counter += 1
                    new_dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                dest_path = new_dest_path

            # Move the file
            shutil.move(src_path, dest_path)
            print(f"Moved file {src_path} to {dest_path}")
        except Exception as e:
            print(f"Error moving file: {e}")





















# import os
# import shutil

# def move_file_to_category_folder(file_path, category):
#     # Define the base directory where files will be categorized
#     base_directory = "/Users/gagankarnati/Documents/CategorizedFiles"
    
#     # Create a category-specific folder inside the base directory
#     category_folder = os.path.join(base_directory, category)
#     os.makedirs(category_folder, exist_ok=True)

#     # Move the file into the category folder
#     try:
#         file_name = os.path.basename(file_path)
#         dest_path = os.path.join(category_folder, file_name)
#         shutil.move(file_path, dest_path)
#         print(f"Moved file {file_path} to {dest_path}")
#         return True
#     except Exception as e:
#         print(f"Error moving file: {e}")
#         return False