# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: login.py
# INFO: Login screen for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 03-06-2024
# Last update: 11-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# PyQt6 Imports
from PyQt6.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGroupBox,
                             QSpacerItem,
                             QSizePolicy,
                             QLineEdit)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

# Custom Imports
from gui.widgets.labelWidget import LabelWidget as Label
from gui.widgets.buttonWidget import ButtonWidget as Button


class LoginScreen(QWidget):
    '''
    Login Screen Class
    '''

    # Define signals which can be emitted to the main window
    login_successful = pyqtSignal(str, str)

    def __init__(self, main_window, window_width=400):
        super().__init__()

        self.main_window = main_window
        self.window_width = window_width
        self.setObjectName("loginScreen")

        # Show login screen
        self.loginScreen()

    def loginScreen(self):
        '''
        Login Box Layout
        '''

        # Create layout
        layout = QHBoxLayout()

        left_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(left_spacer)

        # Add horizontal stretch to center window on screen
        layout.addStretch()

        # Create group box to hold login window elements
        login_box = QGroupBox()
        login_box.setFixedWidth(self.window_width)
        login_box.setObjectName("loginScreenGroupBox")
        login_box_lyt = QVBoxLayout(login_box)

        # Add vertical stretch
        login_box_lyt.addStretch()

        # Create username label
        self.username_lbl = Label(label="Username:",
                                        font_size=12,
                                        align="center")
        login_box_lyt.addWidget(
            self.username_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        # Create username input field
        self.username_input = QLineEdit()
        login_box_lyt.addWidget(
            self.username_input, 0, Qt.AlignmentFlag.AlignCenter)

        # Create password label
        self.password_lbl = Label(label="Password:",
                                        font_size=12,
                                        align="center")
        login_box_lyt.addWidget(
            self.password_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        # Create password input field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        login_box_lyt.addWidget(
            self.password_input, 0, Qt.AlignmentFlag.AlignCenter)

        # Add vertical stretch
        login_box_lyt.addStretch()

        # Create login button
        self.login_button = Button(
            label="Login",
            height=30,
            width=100,
            active=True,
            action=self.login)

        # Create shortcut for the Enter key
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(self.login)

        login_box_lyt.addWidget(
            self.login_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Add login box to layout
        layout.addWidget(login_box)

        # Add horizontal stretch to center window on screen
        layout.addStretch()

        right_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(right_spacer)

        # Set layout
        self.setLayout(layout)

    def clearInputs(self):
        ''' Clear input fields '''
        self.username_input.clear()
        self.password_input.clear()

    def login(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()

        # Here you would check the username and password against your database
        # If the login is successful,
        # emit the login_successful signal with the user type
        # For example:
        if self.checkLogin(self.username, self.password):
            self.userrole = self.getUserType(self.username)
            self.login_successful.emit(self.username, self.userrole)

        # Clear input fields
        self.clearInputs()

    def checkLogin(self, username, password):
        # This is a dummy function to simulate a login check
        if username == "admin" and password == "admin":
            return True
        else:
            return False

    def getUserType(self, username):
        # This is a dummy function to simulate getting the user type
        if username == "admin":
            self.role = "admin"
        elif username == "test":
            self.role = "user"
        else:
            self.role = "viewer"
        return self.role
