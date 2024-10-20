import os

# This is only if the AI version isn't done

aiVersionDone = False

class Organize:
    def __init__(self, folder_file_path):
        if not aiVersionDone:
            self.folder_file_path = folder_file_path
            self.file_types = self.get_file_types()
            self.organize_files()

    def get_file_types(self):
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

    def organize_files(self):
        folder_files = os.listdir(self.folder_file_path)

        for file in folder_files:
            file_extension = os.path.splitext(file)[1][1:]  # Get the extension without the dot
            file_type = self.file_types.get(file_extension)

            if file_type:
                # Create the directory if it doesn't exist
                type_folder_path = os.path.join(self.folder_file_path, file_type)
                if not os.path.exists(type_folder_path):
                    os.mkdir(type_folder_path)

                # Move the file to the respective directory
                old_file_path = os.path.join(self.folder_file_path, file)
                new_file_path = os.path.join(type_folder_path, file)
                os.rename(old_file_path, new_file_path)

