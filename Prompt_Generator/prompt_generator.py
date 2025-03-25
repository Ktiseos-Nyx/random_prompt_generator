# prompt_generator.py

import os
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QPushButton, QTextEdit, QFileDialog,
                             QGroupBox, QListWidget, QListWidgetItem, QSpinBox,
                             QMessageBox)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QDropEvent, QDragEnterEvent
from image_thread import ImageLoadThread
from ui_utils import setup_ui  # Import UI setup function
from file_utils import load_prefixes, load_files, load_images
from settings_manager import SettingsManager
from error_utils import show_error_message  # Import error handling

class PromptGenerator(QWidget):
    imageLoaded = pyqtSignal(object)  # Use object for QPixmap
    imageLoadFailed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        print("Initializing PromptGenerator...")

        self.setWindowTitle("Random Prompt Generator")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)

        # --- Data ---
        self.folder_path = ""
        self.text_files = []
        self.image_files = []
        self.all_words = {}
        self.current_text_file = None
        self.is_shuffling = False
        self.word_limit = 15

        # --- Load Prefixes ---
        self.prefixes_file = "prefixes.json"
        self.prefixes = load_prefixes(self.prefixes_file, show_error_message) #Simplified

        # --- UI Setup ---
        setup_ui(self, self.prefixes) # Pass self and prefixes to setup_ui

        # --- Settings ---
        self.settings_manager = SettingsManager("YourOrganization", "PromptGenerator")
        # No signals connections here
        self.current_thread = None

        self.load_settings()
        self.show()
        print("PromptGenerator initialization complete.")

    # --- UI Update Methods (kept here for simplicity) ---
    def update_prefix_type(self, prefix_type):
        print(f"Updating prefix type to: {prefix_type}")
        self.current_prefix_type = prefix_type
        self.settings_manager.save_setting("prefix", self.current_prefix_type)

    def update_word_limit(self, value):
        print(f"Updating word limit to: {value}")
        self.word_limit = value

    def select_folder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        print(f"Selected folder: {selected_folder}")
        if selected_folder:
            self.set_folder(selected_folder)

    def set_folder(self, folder_path):
        print(f"Setting folder to: {folder_path}")
        if not os.path.isdir(folder_path):
            show_error_message(self,"Invalid folder path.") # Use from error_utils
            return

        self.folder_path = folder_path
        self.folder_label.setText(self.folder_path)
        self.text_files, self.all_words = load_files(self.folder_path, show_error_message)  # Pass error handler
        self.image_files = load_images(self.folder_path)
        self.populate_file_list()
        self.generate_random_prompt()
        self.settings_manager.save_setting("folder", self.folder_path)

    def populate_file_list(self):
        print("Populating file list...")
        self.file_list_widget.clear()
        for filepath in self.text_files:
            item = QListWidgetItem(os.path.basename(filepath))
            item.setData(Qt.ItemDataRole.UserRole, filepath)
            self.file_list_widget.addItem(item)
        print("File list populated.")

    def select_text_file(self, item):
        print(f"Selected text file: {item.data(Qt.ItemDataRole.UserRole)}")
        self.is_shuffling = False
        self.current_text_file = item.data(Qt.ItemDataRole.UserRole)
        self.display_prompt_and_image()

    def display_prompt_and_image(self):
        print("Displaying prompt and image...")
        if self.current_text_file:
            try:
                with open(self.current_text_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()

                print(f"Current prefix type: {self.current_prefix_type}")
                print(f"Available prefixes: {self.prefixes}")
                prefix = random.choice(self.prefixes.get(self.current_prefix_type, []))
                self.prompt_text.setText(f"{prefix} {content}")

                if not self.is_shuffling:
                    self.display_matching_image()

            except OSError as e:
                show_error_message(self,f"Error reading file: {e}") # Use from error_utils
            except KeyError:
                show_error_message(self,f"Prefix '{self.current_prefix_type}' not found in prefixes.json") # Use from error_utils
                self.prompt_text.setText("")
            except IndexError:
                show_error_message(self,f"Prefix List '{self.current_prefix_type}' Is empty.") # Use from error_utils
                self.prompt_text.setText("")

    def display_matching_image(self):
        print("Displaying matching image...")
        if self.current_text_file:
            base_name = os.path.splitext(os.path.basename(self.current_text_file))[0]
            print(f"Looking for image matching: {base_name}")
            matching_image = next((img for img in self.image_files if os.path.splitext(os.path.basename(img))[0] == base_name), None)

            if matching_image:
                self.load_image(matching_image)
            else:
                print("No matching image found.")
                self.image_label.setText("No Matching Image")
        else:
            print("No current text file selected.")
            self.image_label.setText("No Image")

    def load_image(self, image_path):
        """Loads an image using a QThread."""
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.quit()
            self.current_thread.wait()

        self.current_thread = ImageLoadThread(image_path, (self.image_label.width(), self.image_label.height()))
        self.current_thread.imageLoaded.connect(self.set_image)  # Connect HERE
        self.current_thread.imageLoadFailed.connect(self.show_image_error)  # And HERE
        self.current_thread.start()

    def set_image(self, pixmap):
        print("Setting image...")
        self.image_label.setPixmap(pixmap)
        print("Image set.")

    def show_image_error(self, error_message):
        print(f"Image error: {error_message}")
        show_error_message(self, error_message) # Use from error_utils


    def generate_random_prompt(self):
        print("Generating random prompt...")
        self.is_shuffling = False
        if self.text_files:
            self.current_text_file = random.choice(self.text_files)
            for i in range(self.file_list_widget.count()):
                item = self.file_list_widget.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == self.current_text_file:
                    self.file_list_widget.setCurrentItem(item)
                    break
            self.display_prompt_and_image()

    def generate_shuffled_prompt(self):
        print("Generating shuffled prompt...")
        self.is_shuffling = True
        self.current_text_file = None
        self.file_list_widget.setCurrentItem(None)

        if self.all_words:
            words, weights = zip(*self.all_words.items())
            shuffled_words = random.choices(words, weights=weights, k=self.word_limit)
            try:
                prefix = random.choice(self.prefixes.get(self.current_prefix_type, []))
            except KeyError:
                show_error_message(self,f"Prefix '{self.current_prefix_type}' not found in prefixes.json") # Use from error_utils
                prefix = ""
            except IndexError:
                show_error_message(self,f"Prefix List '{self.current_prefix_type}' Is empty.") # Use from error_utils
                prefix = ""
            print(f"Shuffled prompt: {prefix} {' '.join(shuffled_words)}")
            self.prompt_text.setText(f"{prefix} {' '.join(shuffled_words)}")
            self.image_label.setText("No Image (Shuffling)")


    def copy_prompt(self):
        print("Copying prompt to clipboard...")
        clipboard = QApplication.clipboard()
        clipboard.setText(self.prompt_text.toPlainText())
        print("Prompt copied.")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].isLocalFile() and os.path.isdir(urls[0].toLocalFile()):
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        folder_path = event.mimeData().urls()[0].toLocalFile()
        self.set_folder(folder_path)

    def load_settings(self):
        print("Loading settings...")
        self.current_prefix_type = self.settings_manager.load_setting("prefix", list(self.prefixes.keys())[0] if self.prefixes else "")
        if self.current_prefix_type in self.prefixes:
            self.prefix_combo.setCurrentText(self.current_prefix_type)
        else:
            print(f"Saved prefix '{self.current_prefix_type}' not found.")
        folder_path = self.settings_manager.load_setting("folder", "")
        if folder_path:
            self.set_folder(folder_path)
        print("Settings loaded.")

    def closeEvent(self, event):
        print("Closing application...")
        if self.current_thread and self.current_thread.isRunning():
            print("Waiting for thread to finish...")
            self.current_thread.quit()
            self.current_thread.wait()
            print("Thread finished.")
        event.accept()