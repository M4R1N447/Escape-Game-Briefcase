'''
Program Name: Standard QT Framework

Program Description:
This is a basic QT framework which can be used to create a new program.
This program is currently in development.

File: login.py
Function: Login screen Class

Author: Mario Kuijpers
Version: 1.0
Created: 03-06-2024
Last Updated: 24-07-2024

'''

# Imports
from PyQt6.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGroupBox,
                             QSpacerItem,
                             QSizePolicy,
                             QLineEdit)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

from widgets.mainWidgets import LabelWidget
from widgets.buttonWidget import ButtonWidget as Button


class LoginScreen(QWidget):
    '''
    Login Screen Class
    '''

    # Define signals which can be emitted to the main window
    login_successful = pyqtSignal(str, str)

    def __init__(self, main_window, window_width=300):
        super().__init__()

        self.main_window = main_window
        self.window_width = window_width
        self.setObjectName("loginScreen")
        self.initUI()

    def initUI(self):
        '''
        Initialize the User Interface
        '''

        # Create layout
        layout = QHBoxLayout()

        left_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(left_spacer)

        # Add vertical stretch to center window on screen
        layout.addStretch()

        # Create group box to hold login window elements
        login_box = QGroupBox()
        login_box.setFixedWidth(self.window_width)
        login_box.setObjectName("loginScreenGroupBox")
        login_box_lyt = QVBoxLayout(login_box)

        # Create username label
        self.username_lbl = LabelWidget(label="Username:",
                                        font_size=12,
                                        align="center")
        login_box_lyt.addWidget(
            self.username_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        # Create username input field
        self.username_input = QLineEdit()
        login_box_lyt.addWidget(
            self.username_input, 0, Qt.AlignmentFlag.AlignCenter)

        # Create password label
        self.password_lbl = LabelWidget(label="Password:",
                                        font_size=12,
                                        align="center")
        login_box_lyt.addWidget(
            self.password_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        # Create password input field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        login_box_lyt.addWidget(
            self.password_input, 0, Qt.AlignmentFlag.AlignCenter)

        # Create login button
        self.login_button = ButtonWidget(
            label="Login",
            height=30,
            width=100,
            active=True,
            action=self.login)
        login_box_lyt.addWidget(
            self.login_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Add login box to layout
        layout.addWidget(login_box)

        # Add vertical stretch to center window on screen
        layout.addStretch()

        right_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(right_spacer)

        # Set layout
        self.setLayout(layout)

    def login(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()

        # Here you would check the username and password against your database
        # If the login is successful,
        # emit the login_successful signal with the user type
        # For example:
        if self.check_login(self.username, self.password):
            self.userrole = self.get_user_type(self.username)
            self.login_successful.emit(self.username, self.userrole)

    def check_login(self, username, password):
        # This is a dummy function to simulate a login check
        if username == "admin" and password == "admin":
            return True
        else:
            return False

    def get_user_type(self, username):
        # This is a dummy function to simulate getting the user type
        if username == "admin":
            self.role = "admin"
        elif username == "test":
            self.role = "user"
        else:
            self.role = "viewer"
        return self.role
