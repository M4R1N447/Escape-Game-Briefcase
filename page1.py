'''
Program Name: Standard QT Framework

Program Description:
This is a basic QT framework which can be used to create a new program.
This program is currently in development.

File: page1.py
Function: Page 1 example Window

Author: Mario Kuijpers
Version: 1.0
Created: 03-06-2024
Last Updated: 24-07-2024

'''

# Imports
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class Page1(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    page1 = pyqtSignal()
    page2 = pyqtSignal()
    page3 = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.setObjectName("Page 1")
        layout = QHBoxLayout()
        label = QLabel("Page 1")
        button = QPushButton("Page")
        button.clicked.connect(lambda: self.page3.emit())
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
