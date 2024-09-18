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
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout)
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QWindow

from gui.widgets.buttonWidget import ButtonWidget as Button
from gui.widgets.headerWidget import HeaderWidget as Header

import sys
import pygame

# Custom Imports
from functions import createPath


class PygameScreen(QWidget):

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    enter = pyqtSignal()
    mainMenu = pyqtSignal()

    def __init__(self, main_window, screen_dimensions):
        super().__init__()

        self.main_window = main_window
        self.setObjectName("pygameScreen")
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.screen = None
        self.timer = None

        # Create main vertical layout
        self.layout = QVBoxLayout(self)

        # Header Widget
        header = Header(
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="PYGAME TEST")
        self.layout.addWidget(header)

        # Add spacing between splash title label and image
        self.layout.addSpacing(25)

        # Add stretch to push footer to bottom of window
        self.layout.addStretch()

        # Create button layout and widget
        button_lyt = QHBoxLayout()
        button_lyt.addStretch()
        button = Button(object_name="BigButtonWidget",
                        label="START",
                        width=200)
        button.clicked.connect(lambda: self.startPygame())
        button_lyt.addWidget(button)
        button_lyt.addStretch()
        self.layout.addLayout(button_lyt)

        # Create shortcut for the Enter key
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(lambda: self.startPygame())

        # Add spacing between button and bottom of screen
        self.layout.addSpacing(75)

        # Set layout
        self.setLayout(self.layout)

    def startPygame(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width(), self.height()), pygame.NOFRAME)
            pygame.display.set_caption("Pygame in PyQt6")
            self.embedPygame()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updatePygame)
            self.timer.start(16)  # Approximately 60 FPS

    def embedPygame(self):
        window = QWindow.fromWinId(pygame.display.get_wm_info()['window'])
        window.setFlags(Qt.WindowType.FramelessWindowHint)
        window_container = self.createWindowContainer(window, self)
        self.layout().addWidget(window_container)

    def updatePygame(self):
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def resizeEvent(self, event):
        if self.screen:
            self.screen = pygame.display.set_mode((self.width(), self.height()), pygame.NOFRAME)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 with Pygame")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = PygameScreen(self)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
