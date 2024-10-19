import platform

def detect_os():
    """
    Detects the operating system and returns the OS name.
    
    Returns:
        str: A string representing the operating system.
    """
    os_type = platform.system()
    
    if os_type == "Darwin":
        return "MacOS"
    elif os_type == "Windows":
        return "Windows"
    elif os_type == "Linux":
        return "Linux"
    else:
        return "Unsupported OS"

if __name__ == "__main__":
    os_name = detect_os()
    print(f"Detected Operating System: {os_name}")