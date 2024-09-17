# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\widgets\lineEditWidget.py
# INFO: Line Edit Widget Class for Portable Escape Game
#
# Author: Mario Kuijpers
# Start date: 11-09-2024
# Last update: 11-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# PyQt6 Imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtGui import QFont, QIntValidator


class LineEditWidget(QLineEdit):
    '''
    Line Edit Widget Class

    Return Usage:

    self.returnPressed.connect(self.on_return_pressed)
    self.textChanged.connect(self.on_text_changed)
    self.textEdited.connect(self.on_text_edited)
    '''
    def __init__(self,
                 object_name: str = "InputWidget",
                 placeholder: str = None,
                 align: str = "left",
                 font_size: int = 10,
                 input_value: str = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Set object name for styling and identification
        self.setObjectName(object_name)

        # Set placeholder text when provided
        if placeholder:
            self.setPlaceholderText(placeholder)

        # Set alignment
        if align:
            if align == "center":
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif align == "left":
                self.setAlignment(Qt.AlignmentFlag.AlignLeft)
            elif align == "right":
                self.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Set font size
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

        # Set initial input value
        if input_value:
            self.setText(input_value)

    # Set max input length
    def set_max_length(self, max_length):
        self.setMaxLength(max_length)

    # Set input limits for numbers
    def set_validator(self, min_value, max_value):
        self.setValidator(QIntValidator(min_value, max_value))

    # Set a mask for input e.g. '000.000.000.000;_' for IP mask
    def set_input_mask(self, input_mask):
        self.setInputMask(input_mask)


if __name__ == "__main__":
    app = QApplication([])
    widget = LineEditWidget()
    widget.show()
    app.exec()
