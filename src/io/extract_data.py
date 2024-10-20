import os
import stat
import mimetypes
from datetime import datetime

fileInfo = {}

def getMimeType(filePath):
    mimeType, _ = mimetypes.guess_type(filePath)
    return mimeType

def extractData(filePath):
    fileProperties = os.stat(filePath)

    fileSize = fileProperties.st_size
    modificationTime = fileProperties.st_mtime
    accessTime = fileProperties.st_atime
    creationTime = fileProperties.st_birthtime
    filePermissions = fileProperties.st_mode
    fileType = getMimeType(filePath)

    #Convert time to readable format
    modificationTime = datetime.fromtimestamp(modificationTime).isoformat()
    accessTime = datetime.fromtimestamp(accessTime).isoformat()
    creationTime = datetime.fromtimestamp(creationTime).isoformat()
    
    permissions = {
    'Owner': {
        'Read': bool(filePermissions & stat.S_IRUSR),
        'Write': bool(filePermissions & stat.S_IWUSR),
        'Execute': bool(filePermissions & stat.S_IXUSR),
    },
    'Group': {
        'Read': bool(filePermissions & stat.S_IRGRP),
        'Write': bool(filePermissions & stat.S_IWGRP),
        'Execute': bool(filePermissions & stat.S_IXGRP),
    },
    'Others': {
        'Read': bool(filePermissions & stat.S_IROTH),
        'Write': bool(filePermissions & stat.S_IWOTH),
        'Execute': bool(filePermissions & stat.S_IXOTH),
    }
    }

    fileInfo = {
        "File Path": filePath,
        "File Size (bytes)": fileSize,
        "Last Modified": modificationTime,
        "Last Accessed": accessTime,
        "Creation Time": creationTime,
        "File Type": fileType,
        "Permissions": permissions
    }
    return fileInfo

def addToFileInfo(key, value):
    fileInfo[key] = value

print(extractData("test.txt"))