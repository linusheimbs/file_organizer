import os
import shutil

# Define user's Downloads and Documents folders
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")
DOCUMENTS_FOLDER = os.path.expanduser("~/Documents/Sorted_Downloads")


# File type categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Programs": [".exe", ".msi", ".dmg"],
    "Others": []
}


def organize_downloads(source_folder, target_folder):
    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Scan all files in the source folder
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        # Get file extension
        _, ext = os.path.splitext(item)

        # Find the category for the file
        moved = False
        for category, extensions in FILE_CATEGORIES.items():
            if ext.lower() in extensions:
                move_file(item_path, target_folder, category)
                moved = True
                break

        # If no matching category, move to "Others"
        if not moved:
            move_file(item_path, target_folder, "Others")


def move_file(file_path, target_folder, category):
    # Create category folder in the target folder if it doesn't exist
    category_folder = os.path.join(target_folder, category)
    os.makedirs(category_folder, exist_ok=True)

    # Move file to the category folder
    shutil.move(file_path, category_folder)
    print(f"Moved: {file_path} -> {category_folder}")


if __name__ == "__main__":
    organize_downloads(DOWNLOADS_FOLDER, DOCUMENTS_FOLDER)
    print(f"Files sorted into {DOCUMENTS_FOLDER} successfully!")
