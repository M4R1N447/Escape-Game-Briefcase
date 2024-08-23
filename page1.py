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
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

# Import Qt Modules
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QFrame)

from PyQt6.QtGui import (
    QPixmap,
    QFont,
    QIntValidator)

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit)

from widgets.buttonWidget import ButtonWidget as Button
from widgets.labelWidget import LabelWidget as Label


class Page1(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    enter = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setObjectName("Page 1")

        # Show intro screen
        self.introScreen()

    def introScreen(self):
        '''
        introScreen Layout
        '''

        # Create layout
        layout = QHBoxLayout()

        # Add vertical stretch to center window on screen
        layout.addStretch()

        # Create standard header layout
        self.header_lyt = QVBoxLayout()

        # Add spacing between top and header label
        self.header_lyt.addSpacing(10)

        # Header Label Widget
        header = Label(label="Mr Robot")
        self.header_lyt.addWidget(header)

        label = Label("ENTER")
        button = Button("Enter")
        button.clicked.connect(lambda: self.enter.emit())

        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)

        # # Add spacing between header label and title label
        # self.header_lyt.addSpacing(10)

        # # Title Label Widget
        # title = Label(label="#FSOCIETY")
        # self.header_lyt.addWidget(title)

        # # Add spacing between title label and splash label
        # self.header_lyt.addSpacing(75)

        # # Splash Label Widget
        # header_lbl = Label(label=self.label)
        # self.header_lyt.addWidget(header_lbl)

        # self.setLayout(self.header_lyt)

        # # Header Widget
        # header = Label(label="ESCAPE GAME")
        # self.intro_header_lyt.addWidget(header)

        # # Create intro screen image layout
        # self.intro_image_lyt = QHBoxLayout()

        # # Logo Image Widget
        # logo = ImageWidget(
        #     "P:/game/Briefcase Pi 3B/images/mrrobot_small.jpg",
        #     image_height=int(self.screen_height/4),
        #     border=1,
        #     border_color="#9900ff")
        # self.intro_image_lyt.addWidget(logo)
        # self.intro_header_lyt.addLayout(self.intro_image_lyt)

        # # Add stretch between splash label and subtitle label
        # self.intro_header_lyt.addStretch(0)

        # # Warning Label Widget
        # warning = WarningLblWidget(
        #     label=("Warning: Be carefull with the briefcase." +
        #            " \nYou don't need to disassemble anything while playing the game.."))
        # self.intro_header_lyt.addWidget(warning)

        # # Add spacing between title label and splash label
        # self.intro_header_lyt.addSpacing(50)

        # subtitle = SubTitleLblWidget(label="Press 'Start' to begin the game.")
        # self.intro_header_lyt.addWidget(subtitle)

        # # Create button layout
        # self.button_lyt = QHBoxLayout()

        # # Start Button Widget
        # button = ButtonWidget(label="START", action=self.mainMenu)
        # self.button_lyt.addWidget(button)

        # self.intro_scr_lyt = QVBoxLayout()
        # self.intro_scr_lyt.addLayout(self.intro_header_lyt)

        # # Add spacing between header and button layout
        # self.intro_scr_lyt.addSpacing(75)

        # # Add button layout to intro screen layout
        # self.intro_scr_lyt.addLayout(self.button_lyt)

        # # Add spacing between button widget and bottom
        # self.intro_scr_lyt.addSpacing(100)

        # # Add layout to main pygame layout
        # self.welcome_screen_lyt.addLayout(self.intro_scr_lyt)
