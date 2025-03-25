# ui_utils.py (Modified for Side-by-Side Layout)

from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QTextEdit, QGroupBox,
                             QListWidget, QSpinBox, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QSize

def setup_ui(prompt_generator, prefixes):
    """Sets up the UI elements for the PromptGenerator with a side-by-side layout."""

    main_layout = QHBoxLayout()  # Main layout is now horizontal

    # --- Left Side: Controls ---
    controls_layout = QVBoxLayout()

    # --- Prefix Selection ---
    prefix_group = QGroupBox("Prefix")
    prefix_layout = QHBoxLayout()
    prompt_generator.prefix_combo = QComboBox()
    prompt_generator.prefix_combo.addItems(list(prefixes.keys()))
    prompt_generator.prefix_combo.currentTextChanged.connect(prompt_generator.update_prefix_type)
    prefix_layout.addWidget(QLabel("Select Prefix:"))
    prefix_layout.addWidget(prompt_generator.prefix_combo)
    prefix_group.setLayout(prefix_layout)
    controls_layout.addWidget(prefix_group)

    # --- Folder Selection ---
    folder_group = QGroupBox("Folder")
    folder_layout = QHBoxLayout()
    prompt_generator.folder_label = QLabel("No folder selected")
    prompt_generator.folder_button = QPushButton("Select Folder")
    prompt_generator.folder_button.clicked.connect(prompt_generator.select_folder)
    folder_layout.addWidget(prompt_generator.folder_label)
    folder_layout.addWidget(prompt_generator.folder_button)
    folder_group.setLayout(folder_layout)
    controls_layout.addWidget(folder_group)

    # --- Text File List ---
    file_list_group = QGroupBox("Text Files")
    file_list_layout = QVBoxLayout()
    prompt_generator.file_list_widget = QListWidget()
    prompt_generator.file_list_widget.itemClicked.connect(prompt_generator.select_text_file)
    file_list_layout.addWidget(prompt_generator.file_list_widget)
    file_list_group.setLayout(file_list_layout)
    controls_layout.addWidget(file_list_group)

    # --- Word Limit ---
    word_limit_group = QGroupBox("Word Limit")
    word_limit_layout = QHBoxLayout()
    prompt_generator.word_limit_spinbox = QSpinBox()
    prompt_generator.word_limit_spinbox.setMinimum(1)
    prompt_generator.word_limit_spinbox.setMaximum(100)
    prompt_generator.word_limit_spinbox.setValue(prompt_generator.word_limit)
    prompt_generator.word_limit_spinbox.valueChanged.connect(prompt_generator.update_word_limit)
    word_limit_layout.addWidget(QLabel("Max Words:"))
    word_limit_layout.addWidget(prompt_generator.word_limit_spinbox)
    word_limit_group.setLayout(word_limit_layout)
    controls_layout.addWidget(word_limit_group)

    # --- Prompt Display ---
    prompt_group = QGroupBox("Prompt")
    prompt_layout = QVBoxLayout()
    prompt_generator.prompt_text = QTextEdit()
    prompt_generator.prompt_text.setReadOnly(True)
    prompt_generator.copy_button = QPushButton("Copy Prompt")
    prompt_generator.copy_button.clicked.connect(prompt_generator.copy_prompt)
    prompt_generator.shuffle_button = QPushButton("Shuffle Prompt")
    prompt_generator.shuffle_button.clicked.connect(prompt_generator.generate_shuffled_prompt)
    prompt_layout.addWidget(prompt_generator.prompt_text)
    buttons_layout = QHBoxLayout()
    buttons_layout.addWidget(prompt_generator.copy_button)
    buttons_layout.addWidget(prompt_generator.shuffle_button)
    prompt_layout.addLayout(buttons_layout)
    prompt_group.setLayout(prompt_layout)
    controls_layout.addWidget(prompt_group)

    controls_widget = QWidget()  # Create a widget to hold the controls layout
    controls_widget.setLayout(controls_layout)
    main_layout.addWidget(controls_widget)  # Add the controls widget to the main layout


    # --- Right Side: Image ---
    image_layout = QVBoxLayout()
    prompt_generator.image_label = QLabel()
    prompt_generator.image_label.setFixedSize(QSize(400, 400))  # Larger image size!
    prompt_generator.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    image_layout.addWidget(prompt_generator.image_label)

    image_widget = QWidget() # Create a widget to hold the image
    image_widget.setLayout(image_layout)
    main_layout.addWidget(image_widget) # Add the image widget

    prompt_generator.setLayout(main_layout)