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
# Last update: 25-08-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Imports
import sys

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

from PyQt6.QtCore import Qt

# Custom Imports
from functions import createPath
from gui.menuBar import MenuBar
from gui.introScreen import IntroScreen
from gui.login import LoginScreen
from gui.menuScreen import MenuScreen
from gui.page2 import Page2
from gui.page3 import Page3
from gui.widgets.labelWidget import LabelWidget as Label


class MainWindow(QMainWindow):
    '''
    Main Window Class
    '''

    def __init__(self):

        super().__init__()
        self.username = "unknown"
        self.userrole = "unknown"

        # Remove title bar and keep window on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.MaximizeUsingFullscreenGeometryHint)

        # Get screen dimensions
        self.screen_height = QApplication.primaryScreen().size().height()
        self.screen_width = QApplication.primaryScreen().size().width()
        self.screen_dimensions = (self.screen_width, self.screen_height)

        # Set window title
        self.setWindowTitle("Portable Escape Game")

        # Load initial theme
        self.loadTheme(theme="dark_theme.css")

        # Create menu bar at top of screen
        self.createMenuBar()

        # Create main window widget to hold layout
        main_window = QWidget()

        # Create main layout for main window
        layout = QVBoxLayout(main_window)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create content and add to main layout
        self.createContent()
        layout.addWidget(self.content)

        # Create footer and add to main layout
        self.createFooter()
        layout.addWidget(self.footer)

        # Set main window as central widget
        self.setCentralWidget(main_window)

        # Show the window in fullscreen mode
        self.showFullScreen()

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
        menu_bar.intro.connect(lambda: self.switchContent("introScreen"))
        menu_bar.login.connect(lambda: self.switchContent("loginScreen"))
        menu_bar.menu.connect(lambda: self.switchContent("menuScreen"))
        menu_bar.page2.connect(lambda: self.switchContent("Page 2"))
        menu_bar.page3.connect(lambda: self.switchContent("Page 3"))

        # Set PyQt6 MenuBar to this object
        self.setMenuBar(menu_bar)

    def createContent(self):
        '''
        Create content
        '''

        # Create stacked widget for content
        self.content = QStackedWidget()

        # Create intro screen content widget and connect signals to slots
        self.intro_screen = IntroScreen(
            self,
            screen_dimensions=self.screen_dimensions)
        self.content.addWidget(self.intro_screen)
        self.intro_screen.enter.connect(
            lambda: self.switchContent("loginScreen"))

        self.login = LoginScreen(self)
        self.content.addWidget(self.login)
        self.login.login_successful.connect(
            lambda: self.switchContent("menuScreen"))
        # Connect login_successful signal to set_user slot

        # Create intro screen content widget and connect signals to slots
        menu_buttons = [
            {"name": "btn1", "label": "Puzzle Menu", "action": lambda: self.switchContent("introScreen")},
            {"name": "btn2", "label": "Tool Menu", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn3", "label": "Media Menu", "action":lambda: self.switchContent("loginScreen")},
            {"name": "btn4", "label": "Button 4", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn5", "label": "Button 5", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn6", "label": "Button 6", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn7", "label": "Button 7", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn8", "label": "Button 8", "action": lambda: self.switchContent("loginScreen")},
            {"name": "btn9", "label": "Button 9", "action": lambda: self.switchContent("loginScreen")}]

        bottom_buttons = [
            {"name": "back", "label": "Back", "action": lambda: self.switchContent("Page 2")},
            {"name": "exit", "label": "Exit", "action": lambda: self.switchContent("Page 3")}]

        # Create puzzle menu screen
        self.menu_screen = MenuScreen(
            self,
            splash_label="MAIN MENU",
            menu_buttons=menu_buttons,
            bottom_buttons=bottom_buttons)
        self.content.addWidget(self.menu_screen)

        # Create page 2 content widget and connect signals to slots
        self.page2 = Page2(self)
        self.content.addWidget(self.page2)
        self.page2.page3.connect(lambda: self.switchContent("Page 2"))

        # Create page 3 content widget and connect signals to slots
        self.page3 = Page3(self)
        self.content.addWidget(self.page3)
        self.page3.page3.connect(lambda: self.switchContent("Page 3"))

    def createFooter(self):
        '''
        Create footer
        '''

        # Create QWidget to hold layout
        self.footer = QWidget()

        # Create vertical layout
        vert_layout = QVBoxLayout(self.footer)
        vert_layout.setContentsMargins(0, 0, 0, 2)

        # Create horizontal layout
        hor_layout = QHBoxLayout()
        hor_layout.setContentsMargins(0, 0, 0, 2)

        # Create labels and add to horizontal layout
        playername = Label(font_size=12, label="Player: ")
        hor_layout.addWidget(playername)

        playerscore = Label(font_size=12, label="Score: ")
        hor_layout.addWidget(playerscore)

        playerlevel = Label(font_size=12, label="Level: ")
        hor_layout.addWidget(playerlevel)

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

        # Add the horizontal layout to vertical layout
        vert_layout.addLayout(hor_layout)

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
    app = QApplication(sys.argv)
    window = MainWindow()

    # Show window in fullscreen mode
    window.showFullScreen()
    sys.exit(app.exec())
