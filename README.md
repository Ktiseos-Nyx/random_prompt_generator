# Random Prompt Generator with Image Display

This PyQt6 application generates random prompts from text files within a selected folder and displays a corresponding image (if one exists with the same base filename). It's designed for creative tasks, such as generating prompts for AI image generation or writing.

## Features

*   **Folder Selection:** Choose a folder containing `.txt` files and image files.
*   **Prompt Generation:**
    *   Generates a prompt by randomly selecting a text file and prepending a prefix.
    *   Supports shuffling words from all text files within the folder, with a configurable word limit.
*   **Image Display:** Displays an image that matches the selected text file (based on the filename).  Uses Pillow for high-quality image resizing and PyQt for display.
*   **Prefix Selection:** Select a prefix type from a `prefixes.json` file to customize the generated prompts.
*   **Drag and Drop:** Drag and drop a folder onto the application window to select it.
*   **Persistent Settings:** Remembers the last selected folder and prefix type between sessions (using `QSettings`).
*   **Error Handling:** Robust error handling for file access, image loading, and invalid input.
*   **Modular Design:**  Code is well-organized into separate modules for improved maintainability and readability.
*   **Aspect Ratio Preservation:**  Images are resized while maintaining their aspect ratio, preventing distortion.
* **EXIF Handling:** Image rotation is fixed before display.

## Requirements

*   Python 3.7+ (tested with 3.10)
*   PyQt6: `pip install PyQt6`
*   Pillow: `pip install Pillow`

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_name>
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Create a `requirements.txt` file containing `PyQt6` and `Pillow`)

## Usage

1.  **Create a `prefixes.json` file:**  This file defines the available prefix types and their associated prefixes.  Example:

    ```json
    {
      "PonyXL": ["score_9,", "score_8_up,", "score_7_up,", "score_6_up,", "score_5_up,", "score_4_up,"],
      "Illustrious": ["masterpiece,", "very aesthetic,"],
      "Custom": ["My Custom Prefix", "Another Prefix"]
    }
    ```
    Place the file in the same directory as your script.

2.  **Prepare your data folder:** Create a folder containing `.txt` files (one prompt per file) and corresponding image files (e.g., `image1.txt`, `image1.png`). The filenames (without extensions) should match.

3.  **Run the application:**

    ```bash
    python main.py
    ```

4.  **Use the application:**
    *   **Select Folder:** Click "Select Folder" or drag and drop a folder onto the window.
    *   **Select Prefix:** Choose a prefix type from the dropdown menu.
    *   **Text Files:** Click on a text file in the list to display its prompt and matching image.
    *   **Shuffle Prompt:** Click "Shuffle Prompt" to generate a prompt by randomly combining words from all text files.
    *   **Copy Prompt:** Click "Copy Prompt" to copy the generated prompt to the clipboard.
    * **Word Limit**: Adjust the word limit with the up/down arrows.

## Project Structure

The project is organized into the following files:

*   `main.py`: The main application entry point.
*   `prompt_generator.py`: The main widget, handling UI and prompt generation logic.
*   `image_thread.py`: A `QThread` for loading images in the background to prevent UI freezing.
*   `ui_utils.py`: Helper functions for setting up the UI.
*   `file_utils.py`: Helper functions for file and JSON handling.
*   `settings_manager.py`: A class to manage persistent settings.
*   `error_utils.py`: A file to store error checking utilities.
*   `debug_utils.py`: A file to store debug utilities.
*   `prefixes.json`:  A JSON file containing prefix definitions.
*   `requirements.txt`: A list of required libraries

## Troubleshooting

*   **Image not loading:**
    *   Ensure the image file exists and has the same base filename as the corresponding text file.
    *   Check for error messages in the application.
    *   Verify that the image file is not corrupted.
*   **Application crashes:**
    *  Make sure you have the latest versions of PyQt6 and Pillow.
    * Review the console output for error messages.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

We are using the GNU General Public License v3.0
