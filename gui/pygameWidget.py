# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\pygameWidget.py
# INFO: Pygame Widget for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 30-09-2024
# Last update: 30-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Imports
import sys
import pygame

# Import Qt Modules
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence, QImage, QPainter

# Custom Imports
from gui.widgets.buttonWidget import ButtonWidget as Button
from gui.widgets.labelWidget import LabelWidget as Label
from gui.widgets.imageWidget import ImageWidget as Image
from gui.widgets.headerWidget import HeaderWidget as Header


class PygameWidget(QWidget):

    def __init__(self,
                 main_window,
                 screen_dimensions,
                 pygame_width=800,
                 pygame_height=600):
        super().__init__()

        self.main_window = main_window
        self.setObjectName("pygameTest")
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]

        self.pygame_width = pygame_width
        self.pygame_height = pygame_height

        self.initUI()

    def initUI(self):


        # self.setLayout(QVBoxLayout())
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Widget
        header = Header(
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="ESCAPE GAME")
        layout.addWidget(header)

        # Add spacing between splash title label and image
        layout.addStretch()

        # Create a timer to update the Pygame screen
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePygame)
        self.timer.start(16)  # roughly 60 FPS

        pygame.init()
        self.pygame_window = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.is_running = True

        # Initial position and speed of the circle
        self.circle_pos = [100, 100]
        self.circle_speed = [2, 2]


        self.setLayout(layout)

    def updatePygame(self):
        if self.is_running:
            self.pygame_window.fill((0, 0, 0, 0))  # Clear screen with transparent black

            # Update circle position
            self.circle_pos[0] += self.circle_speed[0]
            self.circle_pos[1] += self.circle_speed[1]

            # Bounce the circle off the edges
            if self.circle_pos[0] <= 50 or self.circle_pos[0] >= (self.screen_width-50):
                self.circle_speed[0] = -self.circle_speed[0]
            if self.circle_pos[1] <= 50 or self.circle_pos[1] >= (self.screen_height-50):
                self.circle_speed[1] = -self.circle_speed[1]

            # Draw the circle
            pygame.draw.circle(self.pygame_window, (255, 0, 0), self.circle_pos, 50)
            self.repaint()

    def paintEvent(self, event):
        if self.is_running:
            q_image = self.convertPygameSurfaceToQImage(self.pygame_window)
            painter = QPainter(self)
            painter.drawImage(0, 0, q_image)

    def convertPygameSurfaceToQImage(self, surface):
        width, height = surface.get_size()
        data = surface.get_buffer().raw
        q_image = QImage(data, width, height, QImage.Format.Format_ARGB32)
        return q_image

    def closeEvent(self, event):
        self.is_running = False
        pygame.quit()
        event.accept()
