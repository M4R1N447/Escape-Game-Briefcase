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
# Last update: 02-10-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Imports
import pygame

# Import Qt Modules
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPainter, QColor

# Custom Imports
from gui.widgets.headerWidget import HeaderWidget as Header


class PygameWidget(QWidget):
    '''
    Pygame Widget
    '''
    def __init__(self,
                 main_window,
                 screen_dimensions,
                 object_name="pygameTest",
                 width=1000,
                 height=600,
                 top_margin=100,
                 fps=60):
        super().__init__()

        self.main_window = main_window
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.object_name = object_name
        self.width = width
        self.height = height
        self.top_margin = top_margin
        self.fps = fps

        # Set object name
        self.setObjectName(self.object_name)

        # Initialize Pygame
        self.initUI()

    def initUI(self):
        '''
        Initialize Pygame and create Pygame window
        '''

        # Initialize Pygame
        pygame.init()

        # Create a Pygame window
        self.window = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.running = True

        # Convert fps to milliseconds and create timer to update Pygame screen
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePygame)
        self.timer.start(int(1000 / self.fps))

        # Determine starting position of the game area
        self.x_pos = (((
            self.screen_width - self.width) // 2))
        self.y_pos = (((
            self.screen_height - self.height) // 2) + self.top_margin)

        # Determine game area dimensions
        self.game_width = self.x_pos + self.width
        self.game_height = self.y_pos + self.height

        # Initial position and speed of the circle
        self.circle_pos = [self.x_pos + 100, self.y_pos + 100]
        self.circle_speed = [2, 2]

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Widget
        header = Header(
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="PYGAME TEST WINDOW")
        layout.addWidget(header)

        # Push header to top
        layout.addStretch()

        # Set layout
        self.setLayout(layout)

    def updatePygame(self):
        '''
        Update Pygame screen
        '''
        if self.running:

            # Check for Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen with transparent black
            self.window.fill((0, 0, 0, 0))

            # Draw border around game area
            pygame.draw.rect(
                self.window, (0, 90, 0),
                (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4))

            # Draw background of game area
            pygame.draw.rect(
                self.window, (50, 50, 50),
                (self.x_pos, self.y_pos, self.width, self.height))

            # Update circle position
            self.circle_pos[0] += self.circle_speed[0]
            self.circle_pos[1] += self.circle_speed[1]

            # Check for collisions with margins
            if (self.circle_pos[0] - 50 <
                    self.x_pos or self.circle_pos[0] + 50 > self.game_width):
                self.circle_speed[0] = -self.circle_speed[0]
            if (self.circle_pos[1] - 50 <
                    self.y_pos or self.circle_pos[1] + 50 > self.game_height):
                self.circle_speed[1] = -self.circle_speed[1]

            # Draw the circle
            pygame.draw.circle(self.window, (255, 0, 0), self.circle_pos, 50)
            self.repaint()

    def paintEvent(self, event):
        '''
        Paint event for Pygame screen
        '''
        if self.running:
            q_image = self.convertPygameSurfaceToQImage(self.window)
            painter = QPainter(self)
            painter.drawImage(0, 0, q_image)

    def convertPygameSurfaceToQImage(self, surface):
        ''' Convert Pygame surface to QImage '''
        width, height = surface.get_size()
        data = surface.get_buffer().raw
        q_image = QImage(data, width, height, QImage.Format.Format_ARGB32)
        return q_image

    def closeEvent(self, event):
        ''' Close event for Pygame screen '''
        self.running = False
        pygame.quit()
        event.accept()
