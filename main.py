# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: main.py
# INFO: Main program for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 06-01-2021
# Last update: 09-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

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

# Custom Imports
from functions import createPath
from menuBar import MenuBar
from login import LoginScreen
from page2 import Page2
from page3 import Page3


class MainWindow(QMainWindow):
    '''
    Main Window Class
    '''

    def __init__(self):

        super().__init__()
        self.username = "unknown"
        self.userrole = "unknown"

        # Create main window to hold layout
        main_window = QWidget()

        # Create main layout for main window
        main_layout = QVBoxLayout(main_window)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Set main window as central widget
        self.setCentralWidget(main_window)

        # Set window title
        self.setWindowTitle("Portable Escape Game")

        # Load initial theme
        self.loadTheme(theme="dark_theme.css")

        # Create menu bar at top of screen
        self.createMenuBar()

        # Create header and add to main layout
        self.createHeader()
        main_layout.addWidget(self.header)

        # Add stretch to push header to top of window
        main_layout.addStretch()

        # Create content and add to main layout
        self.createContent()
        main_layout.addWidget(self.content)

        # Add stretch to push footer to bottom of window
        main_layout.addStretch()

        # Create footer and add to main layout
        self.createFooter()
        main_layout.addWidget(self.footer)

    def loadTheme(self, theme=None):
        """
        Load stylesheet for this theme
        """

        # Set theme object to new theme
        self.theme = theme

        # If theme name is None or empty erase current stylesheet
        if self.theme is None or self.theme == "":
            self.setStyleSheet("")
        else:
            # Test if stylesheet can be loaded and load it
            try:
                with open(
                    createPath("themes/") + str(theme), "r",
                        encoding="utf-8") as file:
                    self.setStyleSheet(file.read())
            except (OSError, FileNotFoundError) as error:
                error = error.errno

    def createMenuBar(self):
        '''
        Create menu bar
        '''

        # Create menu bar object
        menu_bar = MenuBar()

        # Connect incoming signals from menuBar.py to their slots
        menu_bar.exit.connect(self.close)
        menu_bar.login.connect(lambda: self.switchContent("loginScreen"))
        menu_bar.page2.connect(lambda: self.switchContent("Page 2"))
        menu_bar.page3.connect(lambda: self.switchContent("Page 3"))

        # Set PyQt6 MenuBar to this object
        self.setMenuBar(menu_bar)

    def createHeader(self):
        '''
        Create header
        '''

        # Create QWidget to hold layout
        self.header = QWidget()

        # Create vertical layout
        vert_layout = QVBoxLayout(self.header)
        vert_layout.setContentsMargins(0, 0, 0, 0)

        # Create horizontal layout
        hor_layout = QHBoxLayout()
        hor_layout.setContentsMargins(0, 0, 0, 0)

        # Create labels and add to horizontal layout
        name_label = QLabel(
            "Header where we can place e.g. icons and the program name")
        hor_layout.addWidget(name_label)

        # Add the horizontal layout to vertical layout
        vert_layout.addLayout(hor_layout)
        vert_layout.addStretch()

        return self.header

    def createContent(self):
        '''
        Create content
        '''

        # Create stacked widget for content
        self.content = QStackedWidget()

        # Create page 1 content widget and connect signals to slots
        self.login = LoginScreen(self)
        self.content.addWidget(self.login)
        self.login.login_successful.connect(
            lambda: self.switchContent("Page 3"))
        # Connect login_successful signal to set_user slot

        # Create page 2 content widget and connect signals to slots
        self.page2 = Page2(self)
        self.content.addWidget(self.page2)
        self.page2.page3.connect(lambda: self.switchContent("Page 3"))

        # Create page 3 content widget and connect signals to slots
        self.page3 = Page3(self)
        self.content.addWidget(self.page3)
        self.page3.page3.connect(lambda: self.switchContent("Page 3"))
        return self.content

    def createFooter(self):
        '''
        Create footer
        '''

        # Create QWidget to hold layout
        self.footer = QWidget()

        # Create vertical layout
        vert_layout = QVBoxLayout(self.footer)
        vert_layout.setContentsMargins(0, 0, 0, 0)

        vert_layout.addStretch()

        # Create horizontal layout
        hor_layout = QHBoxLayout()
        hor_layout.setContentsMargins(0, 0, 0, 0)

        # Create name label and add to horizontal layout
        name_label = QLabel(f"Naam: {self.username}")
        hor_layout.addWidget(name_label)

        # Create and add spacer item
        spacer = QSpacerItem(50, 0, QSizePolicy.Policy.Fixed,
                             QSizePolicy.Policy.Minimum)
        hor_layout.addSpacerItem(spacer)

        # Create role label and add to horizontal layout
        role_label = QLabel(f"Rol: {self.userrole}")
        hor_layout.addWidget(role_label)

        # Add stretch to push content to left of layout
        hor_layout.addStretch()

        # Add the horizontal layout to vertical layout
        vert_layout.addLayout(hor_layout)

        return self.footer

    def switchContent(self, page):
        '''
        Switch to another page in stacked widget self.content
        '''

        # Get index of page
        index = self.content.indexOf(self.content.findChild(QWidget, page))

        # Check if page was found
        if index != -1:
            # Switch to that page
            self.content.setCurrentIndex(index)


# Start application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    # Maximize window with titlebar and top menu
    window.showMaximized()
    app.exec()
