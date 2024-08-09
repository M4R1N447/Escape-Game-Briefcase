# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: widgets\buttonWidget.py
# INFO: Button Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 09-08-2024
# Last update: 09-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QPixmap, QFont)
from PyQt6.QtWidgets import (QWidget,
                             QHBoxLayout,
                             QLabel)
from PyQt6.QtWidgets import (QWidget, QPushButton)


class ButtonWidget(QWidget, QPushButton):
    '''
    Button widget
    '''
    def __init__(self,
                 label: str = "",
                 height: int = 50,
                 width: int = 300,
                 active: bool = True,
                 action=lambda: None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set object name for styling
        self.setObjectName("ButtonWidget")

        self.label = label
        self.active = active
        self.action = action
        self.btn_height = height
        self.btn_width = width

        # Set button size
        if height:
            self.setFixedHeight(self.btn_height)
        if width:
            self.setFixedWidth(self.btn_width)

        # Set button label
        self.setText(label)

        # Set button active state
        self.setEnabled(active)
        self.setCheckable(True)

        # Start action when button is clicked
        self.clicked.connect(lambda _: self.action())

        # Set cursor
        self.updateCursor()

    def setActive(self, active: bool):
        '''
        Set button active / inactive
        '''
        self.active = active
        self.setEnabled(active)
        self.updateCursor()

    def updateCursor(self):
        '''
        Update cursor based on button active state
        '''
        if self.active:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
