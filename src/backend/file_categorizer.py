def categorize_file(file_name):
    """
    Categorizes files based on their extensions.
    Returns a category name (e.g., Documents, Media, etc.).
    """
    if file_name.endswith(".pdf") or file_name.endswith(".docx") or file_name.endswith(".pptx"):
        return "Documents"
    elif file_name.endswith(".mp3") or file_name.endswith(".wav") or file_name(".aac"):
        return"Media_Audio" 
    elif file_name.endswith(".mp4") or file_name.endswith(".avi") or file_name(".mov"):
        return "Media_Video"
    elif file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg") or file_name.endswith(".gif"):
        return "Images"
    elif file_name.endswith(".txt") or file_name.endswith(".csv") or file_name.endswith(".log"):
        return "Text"
    else:
        return "Others"
    
    

    '''
    
    files_extentions = [".pdf", ".docx", ".pptx", ".mp3", ".wav", ".aac" , ".mp4", ".avi" , ".mov", ".jpg", ".png", ".jpeg", ".gif", ".txt", ".csv", ".log"]

    index = 0

    for index in range(files_extentions.len)
        if file_name.endswith(files_extentions[index]).equals(files_extentions[0] or files_extentions[1] or files_extentions[2]):
            return "Documents"
        
        
    
    
    '''