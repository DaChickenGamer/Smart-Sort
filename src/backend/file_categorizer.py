def categorize_file(file_name):
    """
    Categorizes files based on their extensions.
    Returns a category name (e.g., Documents, Media, etc.).
    """
    if file_name.endswith(".pdf"):
        return "Documents"
    elif file_name.endswith(".mp4") or file_name.endswith(".mp3"):
        return "Media"
    elif file_name.endswith(".jpg") or file_name.endswith(".png"):
        return "Images"
    else:
        return "Others"