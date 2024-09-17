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
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt6.QtGui import QShortcut, QKeySequence, QWindow
from PyQt6.QtGui import QPainter, QImage

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

    def __init__(self, main_window, screen_dimensions, parent=None):
        super().__init__(parent)

        self.main_window = main_window
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.setObjectName("pygameScreen")

        self.running = False
        self.screen = None
        self.button_rect = pygame.Rect(300, 250, 200, 100)

        # Set up a timer to call updatePygame at regular intervals
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePygame)
        self.timer.start(16)  # Approximately 60 FPS

    def start_pygame(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        self.parent().hide()

    def stop_pygame(self):
        self.running = False
        pygame.quit()
        self.mainMenu.emit()
        self.parent().show()

    def updatePygame(self):
        if not self.running:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_pygame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.stop_pygame()

        self.screen.fill((255, 255, 255))
        self.draw_button()
        pygame.display.flip()


    def draw_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Back to Menu", True, (0, 0, 255))
        self.screen.blit(text, (self.button_rect.x + 20, self.button_rect.y + 30))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 with Pygame")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = PygameScreen(self)
        self.setCentralWidget(self.central_widget)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Header Widget
        header = Header(
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="PYGAME TEST")
        layout.addWidget(header)

        # Add spacing between splash title label and image
        layout.addSpacing(25)

        self.pygame_widget = PygameScreen(self)
        self.pygame_widget.exit.connect(self.close)  # Connect the signal to the close method
        layout.addWidget(self.pygame_widget)

        # Add stretch to push footer to bottom of window
        layout.addStretch()

        # Create button layout and widget
        button_lyt = QHBoxLayout()
        button_lyt.addStretch()
        button = Button(object_name="BigButtonWidget",
                        label="START",
                        width=200)
        button.clicked.connect(lambda: self.exit.emit())
        button_lyt.addWidget(button)
        button_lyt.addStretch()
        layout.addLayout(button_lyt)

        # Create shortcut for the Enter key
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(lambda: self.exit.emit())

    def closeEvent(self, event):
        pygame.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
