# error_utils.py
from PyQt6.QtWidgets import QMessageBox

def show_error_message(parent, message):
    """Displays an error message using a QMessageBox."""
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(message)
    msg_box.setWindowTitle("Error")
    msg_box.exec()

# Example:  Logging errors to a file (you'd likely use a logging library)
def log_error(message):
    """Logs an error message to a file (basic example)."""
    with open("error_log.txt", "a") as f:
        f.write(f"{message}\n")

# Example:  Function to check file size and show an error if too large
def check_file_size(file_path, max_size_mb, error_callback):
    """
    Checks if the file size exceeds the maximum allowed size.
    Calls error_callback with an error message if it's too large.
    Returns True if the file is OK, False if it's too large.
    """
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        if file_size_mb > max_size_mb:
            error_callback(f"Image file too large ({file_size_mb:.2f} MB).  Please use an image smaller than {max_size_mb}MB.")
            return False  # Indicate file is too large
        return True  # Indicate file size is OK
    except OSError as e:
        error_callback(f"Error checking file size: {e}")
        return False
import os #Needed for filechecks