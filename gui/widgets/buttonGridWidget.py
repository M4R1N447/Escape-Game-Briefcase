# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\widgets\buttonGridWidget.py
# INFO: Button Grid Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 27-08-2024
# Last update: 27-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtWidgets import (QWidget, QGridLayout)

# Custom Imports
from widgets.buttonWidget import ButtonWidget as Button


class ButtonGridWidget(QWidget):
    '''
    Button Grid Widget
    Places buttons from a dictonary in a grid layout
    '''
    def __init__(self,
                 buttons: dict = None,
                 columns: int = 3,
                 hor_spacing: int = 75,
                 vert_spacing: int = 50,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = buttons
        self.columns = columns
        self.hor_spacing = hor_spacing
        self.vert_spacing = vert_spacing

        # Set object name for styling
        self.setObjectName("ButtonGridWidget")

        # Create button grid layout
        self.btn_grid_lyt = QGridLayout()

        # Set horizontal and vertical spacing
        self.btn_grid_lyt.setHorizontalSpacing(self.hor_spacing)
        self.btn_grid_lyt.setVerticalSpacing(self.vert_spacing)

        # Loop through buttons and add to grid layout
        for i, button in enumerate(self.buttons):

            # Calculate row and column in this iteration
            row = i // self.columns
            column = i % self.columns

            # Create button widget
            button["name"] = Button(
                label=button["label"],
                action=button["action"])

            # Add button widget to grid layout
            self.btn_grid_lyt.addWidget(button["name"], row, column)

        self.setLayout(self.btn_grid_lyt)
