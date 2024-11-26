import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

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


def organize_files(source_folder, target_folder):
    try:
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

        messagebox.showinfo("Success", f"Files sorted successfully into {target_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def move_file(file_path, target_folder, category):
    # Create category folder in the target folder if it doesn't exist
    category_folder = os.path.join(target_folder, category)
    os.makedirs(category_folder, exist_ok=True)

    # Move file to the category folder
    shutil.move(file_path, category_folder)


def select_source_folder():
    folder = filedialog.askdirectory(title="Select Source Folder")
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)


def select_target_folder():
    folder = filedialog.askdirectory(title="Select Target Folder")
    if folder:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, folder)


def start_organizing():
    source_folder = source_entry.get()
    target_folder = target_entry.get()
    if not source_folder or not target_folder:
        messagebox.showwarning("Missing Information", "Please select both source and target folders.")
        return

    if not os.path.exists(source_folder):
        messagebox.showerror("Invalid Folder", "The source folder does not exist.")
        return

    organize_files(source_folder, target_folder)


# Create the main UI window
root = tk.Tk()
root.title("File Organizer")

# Source folder selection
tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=10)
source_button = tk.Button(root, text="Browse", command=select_source_folder)
source_button.grid(row=0, column=2, padx=10, pady=10)

# Target folder selection
tk.Label(root, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=1, column=1, padx=10, pady=10)
target_button = tk.Button(root, text="Browse", command=select_target_folder)
target_button.grid(row=1, column=2, padx=10, pady=10)

# Organize button
organize_button = tk.Button(root, text="Organize Files", command=start_organizing, bg="green", fg="white")
organize_button.grid(row=2, column=1, pady=20)

# Run the application
root.mainloop()
