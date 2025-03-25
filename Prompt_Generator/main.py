# main.py
import sys
from PyQt6.QtWidgets import QApplication
from prompt_generator import PromptGenerator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PromptGenerator()
    sys.exit(app.exec())