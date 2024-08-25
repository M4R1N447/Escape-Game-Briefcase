# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: introScreen.py
# INFO: Intro screen for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 03-06-2024
# Last update: 25-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Import Qt Modules
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget
    )

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence

# Custom Imports
from gui.widgets.buttonWidget import ButtonWidget as Button
from gui.widgets.labelWidget import LabelWidget as Label
from gui.widgets.imageWidget import ImageWidget as Image

# Custom Imports
from functions import createPath


class IntroScreen(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    enter = pyqtSignal()

    def __init__(self, main_window, screen_dimensions):
        super().__init__()

        self.main_window = main_window
        self.setObjectName("introScreen")
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]

        # Show intro screen
        self.introScreen()

    def introScreen(self):
        '''
        introScreen Layout
        '''

        # Create main vertical layout
        layout = QVBoxLayout()

        # Add spacing between top of screen and header label
        layout.addSpacing(20)

        # Create header layout and label widget
        header_lyt = QHBoxLayout()
        header_lyt.addStretch()
        header = Label(label="Mr Robot")
        header.setObjectName("HeaderLblWidget")
        header_lyt.addWidget(header)
        header_lyt.addStretch()
        layout.addLayout(header_lyt)

        # Add spacing between header label and title label
        layout.addSpacing(25)

        # Create title layout and label widget
        title_lyt = QHBoxLayout()
        title_lyt.addStretch()
        title = Label(label="#FSOCIETY")
        title.setObjectName("TitleLblWidget")
        title_lyt.addWidget(title)
        title_lyt.addStretch()
        layout.addLayout(title_lyt)

        # Add spacing between title label and splash label
        layout.addSpacing(70)

        # Create splash title layout and label widget
        splash_title_lyt = QHBoxLayout()
        splash_title_lyt.addStretch()
        splash_title = Label(label="ESCAPE GAME")
        splash_title.setObjectName("SplashLblWidget")
        splash_title_lyt.addWidget(splash_title)
        splash_title_lyt.addStretch()
        layout.addLayout(splash_title_lyt)

        # Add spacing between splash title label and image
        layout.addSpacing(75)

        # Create image layout and image widget
        image_lyt = QHBoxLayout()
        image_lyt.addStretch()
        image_file = createPath("images/") + str("mrrobot_small.jpg")
        image = Image(
            image_path=image_file,
            image_height=int(self.screen_height/4))
        image.setObjectName("ImageWidget")
        image_lyt.addWidget(image)
        image_lyt.addStretch()
        layout.addLayout(image_lyt)

        # Add spacing between image and warning
        layout.addSpacing(75)

        # Create title layout and label widget
        warning_lyt = QHBoxLayout()
        warning_lyt.addStretch()
        warning = Label(
            "Warning: Be careful with the briefcase." +
            "\nYou don't need to disassemble anything while playing the game.",
            align="center")
        warning.setObjectName("WarningLblWidget")
        warning_lyt.addWidget(warning)
        warning_lyt.addStretch()
        layout.addLayout(warning_lyt)

        # Add stretch to push footer to bottom of window
        layout.addStretch()

        # Create title layout and label widget
        subtitle_lyt = QHBoxLayout()
        subtitle_lyt.addStretch()
        subtitle = Label(label="Press 'Start' or 'Enter' to begin the game")
        subtitle.setObjectName("SubTitleLblWidget")
        subtitle_lyt.addWidget(subtitle)
        subtitle_lyt.addStretch()
        layout.addLayout(subtitle_lyt)

        # Add spacing between subtitle label and button
        layout.addSpacing(25)

        # Create button layout and widget
        button_lyt = QHBoxLayout()
        button_lyt.addStretch()
        button = Button("START")
        button.setObjectName("BigButtonWidget")
        button.clicked.connect(lambda: self.enter.emit())

        # Create shortcut for the Enter key
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(lambda: self.enter.emit())

        button_lyt.addWidget(button)
        button_lyt.addStretch()
        layout.addLayout(button_lyt)

        # Add spacing between button and bottom of screen
        layout.addSpacing(75)

        # Set layout
        self.setLayout(layout)
