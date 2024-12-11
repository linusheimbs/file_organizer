import os
import shutil
from tkinter import Tk, filedialog, StringVar, BooleanVar, Text
from tkinter import ttk
from ttkthemes import ThemedTk


def log_message(message):
    """Append a message to the status log."""
    status_log.config(state="normal")
    status_log.insert("end", message + "\n")
    status_log.see("end")
    status_log.config(state="disabled")


def sort_files(source_folder, target_folder):
    """ Sort files into target folder by file extension. """
    log_message("Sorting by file type started...")
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):
            file_type = filename.split(".")[-1]
            destination_folder = os.path.join(target_folder, file_type.upper())
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(destination_folder, filename))
            log_message(f"Moved: {filename} -> {destination_folder}")
    log_message("Sorting by file type completed!")


def sort_by_keywords(source_folder, target_folder, keywords, separate_folders):
    """ Sort files into target folder that include a keyword and creates new target folders based on keyword entry. """
    keywords_list = [kw for kw in keywords.split(",") if kw.strip()]
    if not keywords_list:
        log_message("No keywords provided. Sorting aborted.")
        return

    log_message(f"Sorting by keywords: {', '.join(keywords_list)}")
    files_moved = 0  # Counter to track the number of files moved

    for filename in os.listdir(source_folder):
        lower_filename = filename.lower()  # Convert filename to lowercase for comparison
        if any(keyword.strip().lower() in lower_filename for keyword in keywords_list):
            files_moved += 1
            if separate_folders:
                for keyword in keywords_list:
                    if keyword.lower() in lower_filename:
                        keyword_folder = os.path.join(target_folder, keyword)
                        os.makedirs(keyword_folder, exist_ok=True)
                        shutil.move(
                            os.path.join(source_folder, filename),
                            os.path.join(keyword_folder, filename),
                        )
                        log_message(f"Moved: {filename} -> {keyword_folder}")
                        break
            else:
                shutil.move(
                    os.path.join(source_folder, filename),
                    os.path.join(target_folder, filename),
                )
                log_message(f"Moved: {filename} -> {target_folder}")

    if files_moved == 0:
        log_message("No files matching the specified keywords were found.")
    else:
        log_message(f"Sorting by keywords completed! {files_moved} file(s) moved.")


def start_sorting():
    """ Starts the sorting by keywords or file extension. """
    source = source_folder.get()
    target = target_folder.get()
    keywords = keyword_field.get().strip()
    if not source or not target:
        log_message("Source or target folder is not set.")
        return

    if keywords:
        sort_by_keywords(source, target, keywords, separate_folders_var.get())
    else:
        sort_files(source, target)


def select_source_folder():
    """ Sets the folder directory, the user selects, as the source folder. """
    folder = filedialog.askdirectory()
    if folder:
        source_folder.set(folder)
        log_message(f"Selected source folder: {folder}")


def select_target_folder():
    """ Sets the folder directory, the user selects, as the target folder. """
    folder = filedialog.askdirectory()
    if folder:
        target_folder.set(folder)
        log_message(f"Selected target folder: {folder}")


def toggle_checkbox(*_):
    """ Show or hide the checkbox based on keyword entry. """
    if keyword_field.get().strip():
        separate_folders_checkbox.grid(row=3, column=1, sticky="w", padx=10, pady=10)
    else:
        separate_folders_checkbox.grid_forget()


# Main GUI
root = ThemedTk(theme="breeze")
root.title("File Sorter")
root.geometry("800x600")
root.resizable(True, True)

# Configure grid weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=3)
root.grid_columnconfigure(1, weight=1)

style = ttk.Style()
style.configure("TLabel", padding=5, font=("Helvetica", 12))
style.configure("TButton", padding=5, font=("Helvetica", 10))
style.configure("TEntry", padding=5, font=("Helvetica", 10))

source_folder = StringVar()
target_folder = StringVar()
keyword_field = StringVar()
separate_folders_var = BooleanVar(value=False)

# Bind the keyword field to show/hide checkbox dynamically
keyword_field.trace_add("write", toggle_checkbox)

# Layout
ttk.Label(root, text="Source Folder:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
ttk.Entry(root, textvariable=source_folder, width=60).grid(row=0, column=1, padx=10, sticky="ew")
ttk.Button(root, text="Browse", command=select_source_folder).grid(row=0, column=2, padx=10)

ttk.Label(root, text="Target Folder:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
ttk.Entry(root, textvariable=target_folder, width=60).grid(row=1, column=1, padx=10, sticky="ew")
ttk.Button(root, text="Browse", command=select_target_folder).grid(row=1, column=2, padx=10)

ttk.Label(root, text="Keywords (comma-separated):").grid(row=2, column=0, sticky="e", padx=10, pady=10)
ttk.Entry(root, textvariable=keyword_field, width=60).grid(row=2, column=1, padx=10, sticky="ew")

# Checkbox to create folders for each keyword
separate_folders_checkbox = ttk.Checkbutton(
    root, text="Create separate folders for each keyword", variable=separate_folders_var
)

help_text = StringVar()
help_text.set(
    "Enter keywords separated by commas (e.g., report, invoice). "
    "Only files containing these keywords in their names will be moved to the target folder. "
    "Check the box to create separate folders for each keyword."
)
ttk.Label(root, textvariable=help_text, foreground="#555", wraplength=600).grid(
    row=4, column=1, columnspan=2, sticky="w", padx=10, pady=10
)

ttk.Button(root, text="Start Sorting", command=start_sorting).grid(
    row=5, column=1, pady=10, padx=10, ipadx=20, sticky="ew"
)

# Status log
status_log = Text(root, wrap="word", state="disabled", height=10, font=("Helvetica", 10))
status_log.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

root.mainloop()
