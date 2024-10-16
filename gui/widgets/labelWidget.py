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
# Last update: 11-10-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# PyQt6 Imports
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel


class LabelWidget(QLabel):
    '''
    Label Widget Class
    '''
    def __init__(self,
                 parent=None,
                 object_name: str = "LabelWidget",
                 label: str = None,
                 font_color: str = None,
                 font_family: str = None,
                 font_size: int = None,
                 align: str = None,
                 label_width: int = None,
                 label_height: int = None,
                 blink: bool = False,
                 blink_interval: int = 500):

        super().__init__(parent)
        # Set object name for widget identification in stylesheet
        self.setObjectName(object_name)
        self.label = label
        self.font_color = font_color
        self.font_family = font_family
        self.font_size = font_size
        self.align = align
        self.label_width = label_width
        self.label_height = label_height
        self.blink = blink
        self.blink_interval = blink_interval

        # Store original style for reset to default
        self.original_style = self.styleSheet()

        # Initialize blink timer
        self.blink_timer = QTimer(self)

        # Initialize label widget and reset blink
        self.initLabelWidget()
        self.resetBlink()

    def initLabelWidget(self):
        '''
        Initialize label widget parameters
        '''
        # Set label text
        if self.label:
            self.setText(self.label)

        # Set font family, size & color
        if self.font_family or self.font_size or self.font_color:
            stylesheet = ""
            font = QFont()
            if self.font_family:
                stylesheet += f"font-family: {self.font_family};"
                font.setFamily(self.font_family)
            if self.font_size:
                stylesheet += f"font-size: {self.font_size}px;"
                font.setPointSize(self.font_size)
            if self.font_color:
                stylesheet += f"color: {self.font_color};"
            self.setStyleSheet(stylesheet)
            self.setFont(font)

        # Align center when not set left or right
        if self.align:
            alignment = Qt.AlignmentFlag.AlignVCenter
            if self.align == "left":
                alignment |= Qt.AlignmentFlag.AlignLeft
            elif self.align == "right":
                alignment |= Qt.AlignmentFlag.AlignRight
            else:
                alignment |= Qt.AlignmentFlag.AlignHCenter
            self.setAlignment(alignment)

        # Set label width and height
        if self.label_width:
            self.setFixedWidth(self.label_width)
        if self.label_height:
            self.setFixedHeight(self.label_height)

    def toggleVisibility(self):
        '''
        Toggle visibility of label for blinking effect
        '''
        self.setVisible(not self.isVisible())

    def resetBlink(self):
        '''
        Reset blink timer and visibility
        '''
        if self.blink:
            self.blink_timer.timeout.connect(self.toggleVisibility)
            self.blink_timer.start(self.blink_interval)
        else:
            self.blink_timer.stop()
            self.blink_interval = 0
            self.blink = False

    def setLabel(self,
                 label: str = None,
                 font_color: str = None,
                 font_family: str = None,
                 font_size: int = None,
                 align: str = None,
                 width: int = None,
                 height: int = None,
                 blink: bool = False,
                 blink_interval: int = 500):
        '''
        Update label parameters with new parameters
        '''
        # Set new label text
        if label:
            # Reset blink when label changed
            self.resetBlink()
            self.setVisible(True)
            self.setStyleSheet(self.original_style)
            self.label = label
            self.setText(self.label)

        # Set blink parameters
        if blink:
            self.blink = blink
            self.blink_interval = blink_interval
            self.blink_timer.timeout.connect(self.toggleVisibility)
            self.blink_timer.start(self.blink_interval)
        else:
            blink = False
            self.blink = False
            self.resetBlink()

        # Set font family, size & color
        if font_family or font_size or font_color:
            stylesheet = ""
            font = QFont()
            if font_family:
                self.font_family = font_family
                stylesheet += f"font-family: {self.font_family};"
                font.setFamily(self.font_family)
            if font_size:
                self.font_size = font_size
                stylesheet += f"font-size: {self.font_size}px;"
                font.setPointSize(self.font_size)
            if font_color:
                self.font_color = font_color
                stylesheet += f"color: {self.font_color};"
            self.setStyleSheet(stylesheet)
            self.setFont(font)

        # Set alignment if not set then center
        if align:
            self.align = align
            alignment = Qt.AlignmentFlag.AlignVCenter
            if self.align == "left":
                alignment |= Qt.AlignmentFlag.AlignLeft
            elif self.align == "right":
                alignment |= Qt.AlignmentFlag.AlignRight
            else:
                alignment |= Qt.AlignmentFlag.AlignHCenter
            self.setAlignment(alignment)

        # Set label width and height
        if width:
            self.label_width = width
            self.setFixedWidth(self.label_width)
        if height:
            self.label_height = height
            self.setFixedHeight(self.label_height)


if __name__ == "__main__":
    app = QApplication([])
    widget = LabelWidget()
    widget.show()
    app.exec()
