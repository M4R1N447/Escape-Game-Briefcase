# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\widgets\buttonWidget.py
# INFO: Button Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 09-08-2024
# Last update: 02-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton


class ButtonWidget(QPushButton):
    '''
    Button widget Class
    '''

    def __init__(self,
                 object_name: str = "ButtonWidget",
                 label: str = "",
                 height: int = 0,
                 width: int = 0,
                 state: bool = False,
                 state_true_color: str = None,
                 state_true_text_color: str = None,
                 state_false_color: str = "red",
                 state_false_text_color: str = "white",
                 active: bool = True,
                 action=lambda: None):
        super().__init__()

        self.object_name = object_name
        self.label = label
        self.state = state
        self.state_true_color = state_true_color
        self.state_true_text_color = state_true_text_color
        self.state_false_color = state_false_color
        self.state_false_text_color = state_false_text_color
        self.active = active
        self.action = action
        self.btn_height = height
        self.btn_width = width

        # Set object name for styling and identification
        self.setObjectName(self.object_name)

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

    def toggleState(self):
        '''
        Toggle function for button state
        '''
        self.state = not self.state
        color = self.state_true_color if self.state else self.state_false_color
        text_color = (
            self.state_true_text_color if
            self.state else self.state_false_text_color)
        if color and text_color:
            self.setStyleSheet(
                f"background-color: {color}; color: {text_color};")

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
        cursor_shape = (Qt.CursorShape.PointingHandCursor if
                        self.active else Qt.CursorShape.ForbiddenCursor)
        self.setCursor(cursor_shape)


if __name__ == "__main__":
    app = QApplication([])
    widget = ButtonWidget()
    widget.show()
    app.exec()
