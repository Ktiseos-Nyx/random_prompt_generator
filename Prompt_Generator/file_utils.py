# file_utils.py
import os
import json

def load_prefixes(prefixes_file, error_callback):
    """Loads prefixes from a JSON file, handling errors."""
    try:
        if os.path.exists(prefixes_file):
            with open(prefixes_file, "r") as f:
                return json.load(f)
        else:
            with open(prefixes_file, "w") as f:
                default_prefixes = {
                    "PonyXL": ["score_9,", "score_8_up,", "score_7_up,", "score_6_up,", "score_5_up,", "score_4_up,"],
                    "Illustrious": ["masterpiece,", "very aesthetic,"],
                    "Custom": []
                }
                json.dump(default_prefixes, f, indent=2)
                return default_prefixes
    except (json.JSONDecodeError, OSError) as e:
        error_callback(f"Error loading prefixes: {e}")
        return {}


def load_files(folder_path, error_callback):
    """Loads text files and counts words, handling errors."""
    text_files = []
    all_words = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(folder_path, filename)
                text_files.append(filepath)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        words = line.strip().split()
                        for word in words:
                            all_words[word] = all_words.get(word, 0) + 1
    except OSError as e:
        error_callback(f"Error accessing files: {e}")
    return text_files, all_words

def load_images(folder_path):
    """Loads image files from a folder."""
    image_files = []
    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            filepath = os.path.join(folder_path, filename)
            image_files.append(filepath)
    return image_files