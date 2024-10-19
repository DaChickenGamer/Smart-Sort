import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.file_manager import move_file
from backend.file_categorizer import categorize_file

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # When a new file is created, categorize and move it
        file_path = event.src_path
        print(f"New file detected: {file_path}")
        
        # Categorize the file
        category = categorize_file(file_path)
        
        # Define the destination folder based on the category
        if category == "Documents":
            dest_folder = "/Users/gagankarnati/Documents" #"/path/to/Documents"
        elif category == "Media":
            dest_folder = "/Users/gagankarnati/Media" #"/path/to/Media"
        elif category == "Images":
            dest_folder = "/Users/gagankarnati/Images" #"/path/to/Images"
        else:
            dest_folder = "/Users/gagankarnati/Others" #"/path/to/Others"
        
        # Move the file
        move_file(file_path, dest_folder)

def start_monitoring(folder_to_monitor):
    # Set up the observer to watch the specified folder
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_monitor, recursive=False)
    observer.start()
    
    print(f"Started monitoring folder: {folder_to_monitor}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped monitoring.")

    observer.join()