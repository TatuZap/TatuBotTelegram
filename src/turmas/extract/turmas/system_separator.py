import os

# Determines the file separator depending on OS ('\\' for Windows and '/' for Linux)
def sep():
    return '\\' if os.name == 'nt' else '/'