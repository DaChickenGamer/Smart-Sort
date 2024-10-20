import os
import time;

startTime = time.time()

def searchFiles(directory, keyword):
    filePaths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword in file:
                filePaths.append(os.path.join(root, file))
    
    return filePaths

print(searchFiles("C:\\", "te"))

endTime = time.time()
runtime = endTime-startTime

print(f"{runtime:.2f}")