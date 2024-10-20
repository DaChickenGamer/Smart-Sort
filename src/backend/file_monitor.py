import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.file_manager import move_file
from backend.file_categorizer import categorize_file
from ai.openai_utils import categorize_with_ai  # AI-based categorization

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            print(f"New file detected: {file_path}")

            # Categorize the file based on type (Documents, Media, etc.)
            category = categorize_file(file_path)

            # Set the destination folder based on the type category
            if category == "Documents":
                dest_folder = "/Users/gagankarnati/Documents"
            elif category == "Media":
                dest_folder = "/Users/gagankarnati/Media"
            elif category == "Images":
                dest_folder = "/Users/gagankarnati/Images"
            else:
                dest_folder = "/Users/gagankarnati/Others"

            # Move the file to the initial destination folder
            new_file_path = move_file(file_path, dest_folder)

            if new_file_path is not None:
                print(f"Moved file {file_path} to {new_file_path}")

                # AI categorization
                print(f"AI categorization in progress for {file_name}...")
                ai_category = categorize_with_ai(file_name)
                if ai_category:
                    # Convert AI category to a valid folder name
                    ai_folder_name = ai_category.replace(" ", "_").replace("/", "_")
                    final_dest_folder = os.path.join(dest_folder, ai_folder_name)

                    # Ensure the AI-based destination folder exists
                    if not os.path.exists(final_dest_folder):
                        os.makedirs(final_dest_folder)
                        print(f"Created AI category folder: {final_dest_folder}")

                    # Move the file to the AI-based destination folder
                    final_file_path = os.path.join(final_dest_folder, os.path.basename(new_file_path))
                    move_file(new_file_path, final_file_path)
                    print(f"Moved file {new_file_path} to {final_file_path}")
                else:
                    print(f"AI categorization returned no folder for {file_name}, skipping AI-based organization.")
            else:
                print(f"Error: File move failed for {file_path}, skipping AI categorization.")

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

# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file
# from backend.file_categorizer import categorize_file
# from ai.openai_utils import get_gpt_category  # Import the GPT categorization

# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory:
#             file_path = event.src_path
#             print(f"New file detected: {file_path}")

#             # Categorize the file into basic categories (Documents, Media, etc.)
#             category = categorize_file(file_path)

#             # Define the destination folder based on the category
#             if category == "Documents":
#                 dest_folder = "/Users/gagankarnati/Documents"
#             elif category == "Media":
#                 dest_folder = "/Users/gagankarnati/Media"
#             elif category == "Images":
#                 dest_folder = "/Users/gagankarnati/Images"
#             else:
#                 dest_folder = "/Users/gagankarnati/Others"

#             # Move the file to the basic category folder
#             move_file(file_path, dest_folder)

#             # Now apply AI categorization on the file name
#             file_name = os.path.basename(file_path)
#             print(f"Applying AI to categorize: {file_name}")
#             ai_category = get_gpt_category(file_name)  # Use GPT to categorize by title
#             print(f"AI categorized {file_name} as: {ai_category}")

#             # Create subfolder for AI category
#             ai_category_folder = os.path.join(dest_folder, ai_category.replace(" ", "_"))
#             if not os.path.exists(ai_category_folder):
#                 os.makedirs(ai_category_folder)

#             # Move the file into the AI categorized subfolder
#             print(f"Moving file {file_name} to AI folder: {ai_category_folder}")
#             move_file(file_path, ai_category_folder)

# def start_monitoring(folder_to_monitor):
#     # Set up the observer to watch the specified folder
#     event_handler = FileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=folder_to_monitor, recursive=False)
#     observer.start()

#     print(f"Started monitoring folder: {folder_to_monitor}")

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#         print("Stopped monitoring.")
#     observer.join()














# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file
# from backend.file_categorizer import categorize_file
# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         # When a new file is created, categorize and move it
#         file_path = event.src_path
#         print(f"New file detected: {file_path}")
        
#         # Categorize the file
#         category = categorize_file(file_path)
        
#         # Define the destination folder based on the category
#         if category == "Documents":
#             dest_folder = "/Users/gagankarnati/Documents" #"/path/to/Documents"
#         elif category == "Media":
#             dest_folder = "/Users/gagankarnati/Media" #"/path/to/Media"
#         elif category == "Images":
#             dest_folder = "/Users/gagankarnati/Images" #"/path/to/Images"
#         else:
#             dest_folder = "/Users/gagankarnati/Others" #"/path/to/Others"
        
#         # Move the file
#         move_file(file_path, dest_folder)
# def start_monitoring(folder_to_monitor):
#     # Set up the observer to watch the specified folder
#     event_handler = FileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=folder_to_monitor, recursive=False)
#     observer.start()
    
#     print(f"Started monitoring folder: {folder_to_monitor}")
    
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#         print("Stopped monitoring.")
#     observer.join()














# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import time

# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         print(f"File created: {event.src_path}")

# if __name__ == "__main__":
#     observer = Observer()
#     folder_to_monitor = "/Users/gagankarnati/Downloads"  # Change this to your folder path
#     event_handler = FileHandler()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()


















# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from ai.classifier_ai import classify_and_categorize_file  # AI-based classification
# from backend.file_manager import move_file  # Use existing backend file manager

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             time.sleep(3)  # Delay to ensure the file is fully written
#             category, dest_folder = self.classifier(event.src_path)
#             print(f"File categorized as: {category}")
#             try:
#                 move_file(event.src_path, dest_folder)
#             except FileNotFoundError:
#                 print(f"Source file not found: {event.src_path}")

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()



















# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file  # Use backend file manager
# from ai.classifier_ai import classify_and_categorize_file  # AI-based classification

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")

#             # Attempt to ensure the file exists and is fully written
#             if self.wait_for_file(event.src_path):
#                 try:
#                     category, dest_folder = self.classifier(event.src_path)
#                     print(f"File categorized as: {category}")
#                     move_file(event.src_path, dest_folder)  # Move file based on AI category
#                 except Exception as e:
#                     print(f"Error processing file: {e}")
#             else:
#                 print(f"Source file not found or not ready: {event.src_path}")

#     def wait_for_file(self, file_path, timeout=5, check_interval=1):
#         """
#         Wait for the file to be available and stable.
#         - timeout: Total wait time before giving up.
#         - check_interval: Time between each file check.
#         """
#         total_time = 0
#         while total_time < timeout:
#             if os.path.exists(file_path):
#                 try:
#                     # Attempt to open the file to ensure it's fully written and accessible
#                     with open(file_path, 'rb'):
#                         return True
#                 except Exception:
#                     pass
#             time.sleep(check_interval)
#             total_time += check_interval
#         return False

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
















# import os
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file  # Use backend file manager

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             try:
#                 # Call the AI classifier and get the category and destination folder
#                 category, dest_folder = self.classifier(event.src_path)
#                 print(f"File categorized as: {category}")  # Print the category for tracking
                
#                 # Move file to the destination folder
#                 move_file(event.src_path, dest_folder)
#                 print(f"Moved file {event.src_path} to {dest_folder}")
#             except Exception as e:
#                 print(f"Error processing file: {e}")

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             pass  # Keep the observer running indefinitely
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()



















#
#  def wait_for_file_to_stabilize(file_path, timeout=15):
#     """
#     Wait for the file size to stabilize before proceeding.
#     """
#     prev_size = -1
#     stable_time = 0

#     for _ in range(timeout):
#         try:
#             # Check if file exists before checking size
#             if not os.path.exists(file_path):
#                 print(f"File not found: {file_path}")
#                 return False

#             curr_size = os.path.getsize(file_path)
            
#             # If the file size hasn't changed for 3 consecutive checks, consider it stable
#             if curr_size == prev_size:
#                 stable_time += 1
#             else:
#                 stable_time = 0  # Reset the stable time if the size changes

#             if stable_time >= 3:  # If file size is stable for 3 consecutive checks
#                 return True

#             prev_size = curr_size
#             time.sleep(2)  # Wait 2 seconds between checks to give file more time to stabilize
#         except FileNotFoundError:
#             print(f"File not found during stability check: {file_path}")
#             return False
#     return False









# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from ai.classifier_ai import classify_and_categorize_file  # AI-based classification
# from backend.file_manager import move_file  # Use existing backend file manager

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             time.sleep(3)  # Increase delay to 3 seconds to ensure the file is fully written
#             try:
#                 category = self.classifier(event.src_path)  # Call the AI classifier
#                 dest_folder = f"/Users/gagankarnati/{category}"  # Update the path based on your system
#                 move_file(event.src_path, dest_folder)  # Move file based on AI category
#             except Exception as e:
#                 print(f"Error processing file: {e}")

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()






# import os
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file  # Use backend file manager

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             category, dest_folder = self.classifier(event.src_path)
#             print(f"File categorized as: {category}")  # Print the category
#             move_file(event.src_path, dest_folder)  # Move file based on AI category

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()









# import os
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file  # Use existing backend file manager
# from ai.classifier_ai import classify_and_categorize_file  # AI-based classification

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             # Get both category and destination folder from AI classifier
#             category, dest_folder = self.classifier(event.src_path)
#             move_file(event.src_path, dest_folder)  # Use backend file mover

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()










##Working old code. 
# import os
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file  # Use existing backend file manager
# from ai.classifier_ai import classify_and_categorize_file  # AI-based classification

# class FileHandler(FileSystemEventHandler):
#     def __init__(self, classifier):
#         self.classifier = classifier  # AI-based classifier

#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
            
#             # Call the AI classifier and get both category and destination folder
#             category, dest_folder = self.classifier(event.src_path)
            
#             # Move file using the destination folder
#             move_file(event.src_path, dest_folder)  # Use backend file mover

# def start_monitoring(folder_to_monitor, classifier):
#     event_handler = FileHandler(classifier)
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_monitor, recursive=False)
#     observer.start()
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()











#working simple backend code.
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from backend.file_manager import move_file
# from backend.file_categorizer import categorize_file

# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         # When a new file is created, categorize and move it
#         file_path = event.src_path
#         print(f"New file detected: {file_path}")
        
#         # Categorize the file
#         category = categorize_file(file_path)
        
#         # Define the destination folder based on the category
#         if category == "Documents":
#             dest_folder = "/Users/gagankarnati/Documents" #"/path/to/Documents"
#         elif category == "Media":
#             dest_folder = "/Users/gagankarnati/Media" #"/path/to/Media"
#         elif category == "Images":
#             dest_folder = "/Users/gagankarnati/Images" #"/path/to/Images"
#         else:
#             dest_folder = "/Users/gagankarnati/Others" #"/path/to/Others"
        
#         # Move the file
#         move_file(file_path, dest_folder)

# def start_monitoring(folder_to_monitor):
#     # Set up the observer to watch the specified folder
#     event_handler = FileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=folder_to_monitor, recursive=False)
#     observer.start()
    
#     print(f"Started monitoring folder: {folder_to_monitor}")
    
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#         print("Stopped monitoring.")

#     observer.join()