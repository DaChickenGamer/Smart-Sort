import os

from src.io.processed_data import lookup_files_by_file_path, add_file

# This is only if the AI version isn't done

aiVersionDone = False


def get_file_types():
    return {
        "mp4": "video",
        "avi": "video",
        "mkv": "video",
        "mov": "video",
        "wmv": "video",
        "flv": "video",
        "wav": "audio",
        "mp3": "audio",
        "aac": "audio",
        "ogg": "audio",
        "flac": "audio",
        "pdf": "document",
        "doc": "document",
        "docx": "document",
        "xls": "document",
        "xlsx": "document",
        "ppt": "document",
        "pptx": "document",
        "txt": "text",
        "csv": "text",
        "html": "web",
        "css": "web",
        "js": "web",
        "zip": "archive",
        "rar": "archive",
        "tar": "archive",
        "gz": "archive",
    }


def get_category_colors():
    return {
        "video": "red",
        "audio": "blue",
        "document": "green",
        "text": "orange",
        "web": "purple",
        "archive": "brown",
        "other": "gray"
    }


class Organize:
    def __init__(self, folder_file_path):
        if not aiVersionDone:
            self.folder_file_path = folder_file_path
            self.file_types = get_file_types()
            self.organize_files()

    def organize_files(self):
        folder_files = os.listdir(self.folder_file_path)

        for file in folder_files:
            file_extension = os.path.splitext(file)[1][1:]  # Get the extension without the dot
            file_type = self.file_types.get(file_extension)
            file_color = get_category_colors().get(file_type)

            if file_type:
                # Create the directory for the file type if it doesn't exist
                type_folder_path = os.path.join(self.folder_file_path, file_type)  # Only use file_type

                if not os.path.exists(type_folder_path):
                    os.mkdir(type_folder_path)

                # Create a subdirectory for the color if required
                color_folder_path = os.path.join(type_folder_path, file_color)
                if not os.path.exists(color_folder_path):
                    os.mkdir(color_folder_path)

                # Check if file is stored in the DB
                db_file_data = lookup_files_by_file_path(os.path.join(self.folder_file_path, file))

                if db_file_data is None or db_file_data == []:
                    add_file(os.path.join(self.folder_file_path, file), file_extension, file_type,
                             file_color)  # Add color

                # Move the file to the respective directory
                old_file_path = os.path.join(self.folder_file_path, file)
                new_file_path = os.path.join(color_folder_path, file)  # Move to the color directory
                os.rename(old_file_path, new_file_path)
