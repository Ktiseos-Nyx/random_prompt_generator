from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image, UnidentifiedImageError, ImageOps
import os
from error_utils import check_file_size

class ImageLoadThread(QThread):
    imageLoaded = pyqtSignal(QPixmap)
    imageLoadFailed = pyqtSignal(str)

    def __init__(self, image_path, target_size):
        super().__init__()
        self.image_path = image_path
        self.target_size = target_size

    def run(self):
        try:
            if not check_file_size(self.image_path, 50, self.imageLoadFailed.emit):
                return

            img = Image.open(self.image_path)
            img = ImageOps.exif_transpose(img)  # Correct orientation
            width, height = img.size
            target_width, target_height = self.target_size

            # Calculate aspect ratios
            aspect_ratio = width / height
            target_aspect_ratio = target_width / target_height

            # Determine scaling method and calculate new dimensions
            if aspect_ratio > target_aspect_ratio:
                # Wider than target: scale to target width
                new_width = target_width
                new_height = max(1, int(new_width / aspect_ratio))  # Clamp to >= 1
            else:
                # Taller or same aspect ratio: scale to target height
                new_height = target_height
                new_width = max(1, int(new_height * aspect_ratio))  # Clamp to >= 1

            # Resize and convert to QImage/QPixmap
            img = img.resize((new_width, new_height), Image.Resampling.BICUBIC) # Example: Bicubic
            qimage = self.pil_to_qimage(img)

            if aspect_ratio > target_aspect_ratio:
                pixmap = QPixmap.fromImage(qimage).scaledToWidth(target_width, Qt.TransformationMode.SmoothTransformation)
            else:
                pixmap = QPixmap.fromImage(qimage).scaledToHeight(target_height, Qt.TransformationMode.SmoothTransformation)

            self.imageLoaded.emit(pixmap)


        except FileNotFoundError:
            self.imageLoadFailed.emit(f"Image file not found: {self.image_path}")
        except UnidentifiedImageError:
            self.imageLoadFailed.emit(f"Could not open or read image: {self.image_path}")
        except ValueError as e:
            self.imageLoadFailed.emit(str(e))
        except Exception as e:
            self.imageLoadFailed.emit(f"An unexpected error occurred: {e}")

    def pil_to_qimage(self, img):
        """Helper function to convert a PIL Image to a QImage."""
        if img.mode == 'RGBA':
            qimage = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format.Format_RGBA8888)
        elif img.mode == 'RGB':
            qimage = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format.Format_RGB888)
        elif img.mode == 'L':
            qimage = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format.Format_Grayscale8)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        return qimage