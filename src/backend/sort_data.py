import os;

def sortData(directory):
    files = os.listdir(directory)
    files.sort()

    return files

print(sortData("C:\\"))