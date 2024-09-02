# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\widgets\labelWidget.py
# INFO: Label Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 11-08-2024
# Last update: 02-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class LabelWidget(QLabel):
    '''
    Label Widget Class
    '''
    def __init__(self,
                 label: str = "",
                 font_size: int = None,
                 align: str = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.label = label
        self.font_size = font_size

        # Set object name for styling
        self.setObjectName("LabelWidget")

        # Set label text
        self.setText(self.label)

        # Set font size
        if font_size:
            font = QFont()
            font.setPointSize(self.font_size)
            self.setFont(font)

        # Set alignment
        if align:
            if align == "center":
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif align == "left":
                self.setAlignment(Qt.AlignmentFlag.AlignLeft)
            elif align == "right":
                self.setAlignment(Qt.AlignmentFlag.AlignRight)
