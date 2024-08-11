'''
Program Name: Test Hardware Management System

Program Description:
This program is a test hardware management system
which can be used to manage hardware components.
This program is currently in development.

File: widgets/mainWidgets.py
Function: Main Widgets Class

Author: Mario Kuijpers
Version: 1.0
Created: 21-06-2024
Last Updated: 21-06-2024

'''

# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QPixmap, QFont)
from PyQt6.QtWidgets import (QWidget,
                             QHBoxLayout,
                             QLabel)


class ImageWidget(QWidget):
    '''
    Image Widget Class
    '''
    def __init__(self,
                 image_path: str = None,
                 image_height: int = None,
                 image_width: int = None,
                 border: int = 0,
                 border_color: str = "#00ff00",
                 align: str = "center",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_path = image_path
        self.image_height = image_height
        self.image_width = image_width
        self.border = border
        self.border_color = border_color
        self.align = align

        # Set object name for styling
        self.setObjectName("ImageWidget")

        # Load the image into a QPixmap
        pixmap = QPixmap(image_path)

        # Resize the label or the image
        if self.image_height is not None:
            pixmap = pixmap.scaledToHeight(self.image_height)
        else:
            self.image_height = pixmap.height()

        if self.image_width is not None:
            pixmap = pixmap.scaledToWidth(self.image_width)
        else:
            self.image_width = pixmap.width()

        # Create a QLabel for the image
        self.image_label = QLabel(self)

        # Set the QPixmap to the QLabel
        self.image_label.setPixmap(pixmap)

        # Center the image
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Set the width & height of the widget
        self.setFixedHeight(self.image_height)
        self.setFixedWidth(self.image_width)

        # Create and align layout
        self.image_wgt_lyt = QHBoxLayout()
        self.image_wgt_lyt.addWidget(self.image_label)
        self.image_wgt_lyt.setAlignment(
            Qt.AlignmentFlag.AlignTop |
            Qt.AlignmentFlag.AlignHCenter)
        self.image_wgt_lyt.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.image_wgt_lyt)
