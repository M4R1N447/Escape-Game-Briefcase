# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\emptyScreen.py
# INFO: Empty screen for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 03-06-2024
# Last update: 28-09-2024
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


class EmptyScreen(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()

    def __init__(self, main_window, screen_dimensions):
        super().__init__()

        # Set main window
        self.main_window = main_window
        self.setObjectName("emptyScreen")
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]

        # Show empty screen
        self.emptyScreen()

    def emptyScreen(self):
        '''
        emptyScreen Layout
        '''

        # Create main vertical layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Add stretch
        layout.addStretch()

        # Create button layout and widget
        button_lyt = QHBoxLayout()
        button_lyt.setContentsMargins(0, 0, 0, 0)
        button_lyt.addStretch()
        button = Button(object_name="BigButtonWidget",
                        label="BACK",
                        width=200)
        button.clicked.connect(lambda: self.exit.emit())

        # Create shortcut for the Enter key
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(lambda: self.exit.emit())

        button_lyt.addWidget(button)
        button_lyt.addStretch()
        layout.addLayout(button_lyt)

        # Add spacing between button and bottom of screen
        layout.addSpacing(75)

        # Set layout
        self.setLayout(layout)
