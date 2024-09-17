# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\messageBox.py
# INFO: Message Box Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 17-09-2024
# Last update: 17-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout)
from PyQt6.QtGui import QShortcut, QKeySequence

# Custom Imports
from widgets.labelWidget import LabelWidget as Label
from widgets.buttonWidget import ButtonWidget as Button


class MessageBox(QMainWindow):
    """
    Message Box Class
    """

    # Define signals which can be emitted to the main window
    button_pressed = pyqtSignal()

    def __init__(self,
                 object_name: str = "MessageBox",
                 width=500,
                 height=200,
                 opacity=0.85,
                 message=None,
                 message_size=14,
                 button_label=None,
                 button_height=30,
                 button_width=125,
                 lbl_btn_spacer=0,
                 title="Message Box"):

        super().__init__()
        self.object_name = object_name
        self.window_width = width
        self.window_height = height
        self.window_opacity = opacity
        self.message = message
        self.message_size = message_size
        self.button_label = button_label
        self.button_height = button_height
        self.button_width = button_width
        self.lbl_btn_spacer = lbl_btn_spacer
        self.title = title

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Set window size
        self.setGeometry(100, 100, self.window_width, self.window_height)

        # Set object name for styling and identification
        self.setObjectName(self.object_name)

        # Set window title if provided
        if self.title:
            self.setWindowTitle(self.title)
        else:
            # Remove window title
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # Move popup to center of screen
        self.popup_rect = self.frameGeometry()
        self.popup_center = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        self.popup_rect.moveCenter(self.popup_center)
        self.move(self.popup_rect.topLeft())

        # Set styling of popup window
        self.setWindowOpacity(self.window_opacity)

        # Set background color
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create message box layout
        self.popup_layout = QVBoxLayout()

        # Add stretch to center items
        self.popup_layout.addStretch()

        # Create message label if message is provided
        if self.message:
            self.label = Label(label=self.message,
                               font_size=self.message_size,
                               align="center")
            self.popup_layout.addWidget(self.label)

        # Create button if button label is provided
        if self.button_label:

            # Create spacing between message and button
            self.popup_layout.addSpacing(self.lbl_btn_spacer)

            # Create button if button label is provided
            self.button_layout = QHBoxLayout()

            # Add stretch to center items
            self.button_layout.addStretch()

            self.button = Button(label=self.button_label,
                                 height=self.button_height,
                                 width=self.button_width,
                                 action=self.buttonPressed)

            # Create shortcut for the Enter key
            enter_shortcut = QShortcut(QKeySequence("Return"), self)
            enter_shortcut.activated.connect(self.buttonPressed)
            self.button_layout.addWidget(self.button)

            # Add stretch to center items
            self.button_layout.addStretch()
            self.popup_layout.addLayout(self.button_layout)

        # Add stretch to center items
        self.popup_layout.addStretch()

        # Set layout
        self.centralWidget.setLayout(self.popup_layout)

        # Show Popup
        self.show()

    # Emit signal when button is pressed and close message box
    def buttonPressed(self):
        self.button_pressed.emit()
        self.close()

    # Close message box
    def close_window(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MessageBox()
    window.show()
    app.exec()
