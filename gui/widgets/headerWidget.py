# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\widgets\headerWidget.py
# INFO: Header Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 16-03-2024
# Last update: 24-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout)

# Custom Imports
from gui.widgets.labelWidget import LabelWidget as Label


class HeaderWidget(QWidget):
    '''
    Standard Header Widget
    '''
    def __init__(self,
                 header_label: str = "Mr Robot",
                 title_label: str = "#FSOCIETY",
                 splash_label: str = "ESCAPE GAME",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = header_label
        self.title_label = title_label
        self.splash_label = splash_label

        # Set object name for styling
        self.setObjectName("HeaderWidget")

        # Create standard header layout
        layout = QVBoxLayout()

        # Add spacing between top of screen and header label
        layout.addSpacing(10)

        # Create header layout and label widget
        header_lyt = QHBoxLayout()
        header_lyt.addStretch()
        header = Label(label=self.header_label)
        header.setObjectName("HeaderLblWidget")
        header_lyt.addWidget(header)
        header_lyt.addStretch()
        layout.addLayout(header_lyt)

        # Add spacing between header label and title label
        layout.addSpacing(15)

        # Create title layout and label widget
        title_lyt = QHBoxLayout()
        title_lyt.addStretch()
        title = Label(label=self.title_label)
        title.setObjectName("TitleLblWidget")
        title_lyt.addWidget(title)
        title_lyt.addStretch()
        layout.addLayout(title_lyt)

        # Add spacing between title label and splash label
        layout.addSpacing(75)

        # Create splash title layout and label widget
        splash_title_lyt = QHBoxLayout()
        splash_title_lyt.addStretch()
        splash_title = Label(label=self.splash_label)
        splash_title.setObjectName("SplashLblWidget")
        splash_title_lyt.addWidget(splash_title)
        splash_title_lyt.addStretch()
        layout.addLayout(splash_title_lyt)

        # Add spacing between splash title label and image
        layout.addSpacing(25)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    widget = HeaderWidget()
    widget.show()
    app.exec()
