# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: page2.py
# INFO: Intro screen for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 03-06-2024
# Last update: 25-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Imports
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class Page2(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    page1 = pyqtSignal()
    page2 = pyqtSignal()
    page3 = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.setObjectName("Page 2")
        layout = QHBoxLayout()
        label = QLabel("Page 2")
        button = QPushButton("Page")
        button.clicked.connect(lambda: self.page3.emit())
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
