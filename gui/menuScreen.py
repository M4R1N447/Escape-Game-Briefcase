# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\menuScreen.py
# INFO: Menu Screen Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 27-08-2024
# Last update: 27-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtWidgets import (QWidget, QGridLayout)

# PyQt6 Imports
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QStackedWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QSpacerItem,
                             QSizePolicy,
                             QLabel)

from PyQt6.QtCore import Qt

# Custom Imports
from widgets.buttonGridWidget import ButtonGridWidget as ButtonGrid


class MenuScreen(QWidget):
    '''
    Menu Screen Widget
    Create a complete menu screen with header, buttons and bottom buttons
    '''
    def __init__(self,
                 object_name: str = "MenuScreen",
                 header_label: str = None,
                 menu_buttons: dict = None,
                 bottom_buttons: dict = None,
                 menu_btn_columns: int = 3,
                 bot_btn_columns: int = 2,
                 hor_spacing: int = 75,
                 vert_spacing: int = 50,
                 bot_btn_spacing: int = 50,
                 bot_screen_spacing: int = 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.object_name = object_name
        self.header_label = header_label
        self.menu_buttons = menu_buttons
        self.bottom_buttons = bottom_buttons
        self.menu_btn_columns = menu_btn_columns
        self.bot_btn_columns = bot_btn_columns
        self.hor_spacing = hor_spacing
        self.vert_spacing = vert_spacing
        self.bot_btn_spacing = bot_btn_spacing
        self.bot_screen_spacing = bot_screen_spacing

        # Set object name for styling
        self.setObjectName(self.object_name)

        # Create menu screen layout
        self.menu_screen_lyt = QVBoxLayout()

        # Header Widget
        header = HeaderWidget(label=self.header_label)
        self.menu_screen_lyt.addWidget(header)

        # Add stretch between header and menu buttons
        self.menu_screen_lyt.addStretch(0)

        # Create menu buttons
        if menu_buttons:
            menu_btn_grid = ButtonGrid(
                buttons=self.menu_buttons,
                columns=self.menu_btn_columns,
                hor_spacing=self.hor_spacing,
                vert_spacing=self.vert_spacing)
            self.menu_screen_lyt.addWidget(menu_btn_grid)

            # Add spacing between menu and bottom buttons
            self.menu_screen_lyt.addSpacing(self.bot_btn_spacing)

        # Create bottom buttons layout
        if bottom_buttons:
            bottom_btn_grid = ButtonGrid(
                buttons=self.bottom_buttons,
                columns=self.bot_btn_columns,
                hor_spacing=self.hor_spacing,
                vert_spacing=self.vert_spacing)
            self.menu_screen_lyt.addWidget(bottom_btn_grid)

        # Add spacing between buttons and bottom of screen
        self.menu_screen_lyt.addSpacing(self.bot_screen_spacing)

        self.setLayout(self.menu_screen_lyt)
