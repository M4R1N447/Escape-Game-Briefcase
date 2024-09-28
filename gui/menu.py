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
# Last update: 28-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)

# Custom Imports
from gui.widgets.buttonGridWidget import ButtonGridWidget as ButtonGrid
from gui.widgets.headerWidget import HeaderWidget as Header


class Menu(QWidget):
    '''
    Menu Screen Widget
    Create a complete menu screen with header, buttons and bottom buttons
    '''

    def __init__(self,
                 object_name: str = "menuScreen",
                 header_label: str = "Mr Robot",
                 title_label: str = "#FSOCIETY",
                 splash_label: str = "ESCAPE GAME",
                 menu_buttons: dict = None,
                 bottom_buttons: dict = None,
                 menu_btn_columns: int = 3,
                 bot_btn_columns: int = 2,
                 menu_side_spacing: int = 75,
                 hor_spacing: int = 100,
                 vert_spacing: int = 50,
                 bot_btn_spacing: int = 50,
                 bot_screen_spacing: int = 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.object_name = object_name
        self.header_label = header_label
        self.title_label = title_label
        self.splash_label = splash_label
        self.menu_buttons = menu_buttons
        self.bottom_buttons = bottom_buttons
        self.menu_btn_columns = menu_btn_columns
        self.bot_btn_columns = bot_btn_columns
        self.menu_side_spacing = menu_side_spacing
        self.hor_spacing = hor_spacing
        self.vert_spacing = vert_spacing
        self.bot_btn_spacing = bot_btn_spacing
        self.bot_screen_spacing = bot_screen_spacing

        # Set object name for styling
        self.setObjectName(self.object_name)

        # Create main vertical layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Widget
        header = Header(
            header_label=self.header_label,
            title_label=self.title_label,
            splash_label=self.splash_label)
        layout.addWidget(header)

        # Add stretch between header and menu buttons
        layout.addStretch(0)

        # Create horizontal layout
        horizontal_lyt = QHBoxLayout()
        horizontal_lyt.setContentsMargins(0, 0, 0, 0)

        # Add spacing between left screen side and menu buttons
        horizontal_lyt.addSpacing(self.menu_side_spacing)

        # Create vertical layout
        vertical_lyt = QVBoxLayout()
        vertical_lyt.setContentsMargins(0, 0, 0, 0)

        # Create menu buttons
        if menu_buttons:
            menu_btn_grid = ButtonGrid(
                buttons=self.menu_buttons,
                columns=self.menu_btn_columns,
                hor_spacing=self.hor_spacing,
                vert_spacing=self.vert_spacing)
            vertical_lyt.addWidget(menu_btn_grid)

            # Add spacing between menu and bottom buttons
            vertical_lyt.addSpacing(self.bot_btn_spacing)

        # Create bottom buttons
        if bottom_buttons:
            bottom_btn_grid = ButtonGrid(
                buttons=self.bottom_buttons,
                columns=self.bot_btn_columns,
                hor_spacing=self.hor_spacing,
                vert_spacing=self.vert_spacing)
            vertical_lyt.addWidget(bottom_btn_grid)

        # Add vertical layout to horizontal layout
        horizontal_lyt.addLayout(vertical_lyt)

        # Add spacing between right screen side and menu buttons
        horizontal_lyt.addSpacing(self.menu_side_spacing)

        # Add horizontal layout to main layout
        layout.addLayout(horizontal_lyt)

        # Add spacing between menu and bottom of screen
        layout.addSpacing(self.bot_screen_spacing)

        # Set layout
        self.setLayout(layout)
