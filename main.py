import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def sort_files(source_folder, target_folder, keyword=None):
    try:
        # Create target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        files_moved = 0

        # Loop through all files in the source folder
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)

            # Skip directories
            if os.path.isdir(source_path):
                continue

            # Move files by keyword if provided
            if keyword:
                if keyword.lower() in filename.lower():
                    shutil.move(source_path, os.path.join(target_folder, filename))
                    files_moved += 1
            # Otherwise, sort by file type
            else:
                file_extension = os.path.splitext(filename)[1].lower()
                folder_by_type = os.path.join(target_folder, file_extension[1:] if file_extension else "other")
                os.makedirs(folder_by_type, exist_ok=True)
                shutil.move(source_path, os.path.join(folder_by_type, filename))
                files_moved += 1

        messagebox.showinfo("Success", f"{files_moved} file(s) moved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def browse_folder(entry_field):
    folder = filedialog.askdirectory()
    if folder:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, folder)


def run_sorter():
    source_folder = source_entry.get()
    target_folder = target_entry.get()
    keyword = keyword_entry.get().strip()

    if not source_folder or not target_folder:
        messagebox.showwarning("Input Error", "Please select both source and target folders.")
        return

    sort_files(source_folder, target_folder, keyword if keyword else None)


# Create the GUI
root = tk.Tk()
root.title("File Sorting Program")

# Source folder
tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_folder(source_entry)).grid(row=0, column=2, padx=10, pady=5)

# Target folder
tk.Label(root, text="Target Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_folder(target_entry)).grid(row=1, column=2, padx=10, pady=5)

# Keyword (optional)
tk.Label(root, text="Keyword (optional):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
keyword_entry = tk.Entry(root, width=50)
keyword_entry.grid(row=2, column=1, padx=10, pady=5)

# Run button
tk.Button(root, text="Sort Files", command=run_sorter).grid(row=3, column=0, columnspan=3, pady=20)

# Run the application
root.mainloop()
