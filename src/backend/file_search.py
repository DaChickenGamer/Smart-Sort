import os

def search_files(keyword):
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if keyword in file:
                yield os.path.join(root, file)