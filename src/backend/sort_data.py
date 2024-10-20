import os

def sort_data(directory):
    files = os.listdir(directory)
    files.sort()

    return files