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
# Last update: 03-09-2024
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
from gui.menu import Menu
from gui.page2 import Page2
from gui.page3 import Page3
from gui.widgets.labelWidget import LabelWidget as Label

# Puzzle imports
# from puzzles.memory.memory import Game as memory
from gui.pygameWidget import PygameWidget
# from puzzles.memory.memory2 import Memory
from gui.pygameScreen import PygameScreen


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
        self.screen_height = QApplication.primaryScreen().size().height() - 50
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
        self.content.setObjectName("mainContent")
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
                    createPath("gui/themes/") + str(theme), "r",
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
        menu_bar.mainMenu.connect(lambda: self.switchContent("mainMenu"))
        menu_bar.puzzleMenu.connect(lambda: self.switchContent("puzzleMenu"))
        menu_bar.toolMenu.connect(lambda: self.switchContent("toolMenu"))
        menu_bar.mediaMenu.connect(lambda: self.switchContent("mediaMenu"))
        menu_bar.page2.connect(lambda: self.switchContent("Page 2"))
        menu_bar.page3.connect(lambda: self.switchContent("Page 3"))

        # Set PyQt6 MenuBar to this object
        self.setMenuBar(menu_bar)

    def createContent(self):
        '''
        Create all content pages
        '''

        # Create main layout for main window
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

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
            lambda: self.switchContent("mainMenu"))
        # Connect login_successful signal to set_user slot

        # Create main menu widget
        self.main_menu = self.createMainMenu()
        self.content.addWidget(self.main_menu)

        # Create puzzle menu widget
        self.puzzle_menu = self.createPuzzleMenu()
        self.content.addWidget(self.puzzle_menu)

        # Create puzzle menu widget
        self.tool_menu = self.createToolMenu()
        self.content.addWidget(self.tool_menu)

        # Create media menu widget
        self.media_menu = self.createMediaMenu()
        self.content.addWidget(self.media_menu)

        # Create page 2 content widget and connect signals to slots
        self.page2 = Page2(self)
        self.content.addWidget(self.page2)
        self.page2.page3.connect(lambda: self.switchContent("Page 2"))

        # Create intro screen content widget and connect signals to slots
        self.pygame_test = PygameWidget(self, screen_dimensions=self.screen_dimensions)
        self.content.addWidget(self.pygame_test)

        # Create intro screen content widget and connect signals to slots
        self.pygame_screen = PygameScreen(self, screen_dimensions=self.screen_dimensions)
        self.content.addWidget(self.pygame_screen)

        # Create intro screen content widget and connect signals to slots
        # self.memory = Memory(self, screen_dimensions=self.screen_dimensions)
        # self.content.addWidget(self.memory)

        # Create page 3 content widget and connect signals to slots
        self.page3 = Page3(self)
        self.content.addWidget(self.page3)
        self.page3.page3.connect(lambda: self.switchContent("Page 3"))

        layout.addWidget(self.content)
        layout.addStretch()

        return layout

    def createMainMenu(self):
        # Create button list for Main Menu
        main_menu_buttons = [
            {"id": "btn1", "lbl": "Puzzle Menu", "action": lambda: self.switchContent("puzzleMenu")},
            {"id": "btn2", "lbl": "Tool Menu", "action": lambda: self.switchContent("toolMenu")},
            {"id": "btn3", "lbl": "Media Menu", "action": lambda: self.switchContent("mediaMenu")},
            {"id": "btn4", "lbl": "Button 4", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn5", "lbl": "Button 5", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn6", "lbl": "Button 6", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn7", "lbl": "Button 7", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn8", "lbl": "Button 8", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn9", "lbl": "Button 9", "action": lambda: self.switchContent("loginScreen")}]

        # Create button list for Main Menu bottom buttons
        main_menu_bottom_buttons = [
            {"id": "back", "lbl": "Back", "action": lambda: self.switchContent("loginScreen")},
            {"id": "exit", "lbl": "Exit", "action": lambda: self.switchContent("introScreen")}]

        # Create Main Menu screen with all buttons
        self.main_menu_screen = Menu(
            object_name="mainMenu",
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="MAIN MENU",
            menu_buttons=main_menu_buttons,
            bottom_buttons=main_menu_bottom_buttons)
        return self.main_menu_screen

    def createPuzzleMenu(self):
        # Create button list for Puzzle Menu
        puzzle_menu_buttons = [
            {"id": "btn1", "lbl": "Memory", "action": lambda: self.switchContent("pygameTest")},
            {"id": "btn2", "lbl": "Pygame Test", "action": lambda: self.switchContent("pygameTest")},
            {"id": "btn3", "lbl": "Empty Screen ", "action": lambda: self.switchContent("emptyScreen")},
            {"id": "btn4", "lbl": "NEW TEST", "action": lambda: self.switchContent("pygameScreen")},
            {"id": "btn5", "lbl": "Puzzle 5", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn6", "lbl": "Puzzle 6", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn7", "lbl": "Puzzle 7", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn8", "lbl": "Puzzle 8", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn9", "lbl": "Puzzle 9", "action": lambda: self.switchContent("loginScreen")}]

        # Create button list for bottom buttons
        puzzle_menu_bottom_buttons = [
            {"id": "back", "lbl": "Back", "action": lambda: self.switchContent("mainMenu")},
            {"id": "exit", "lbl": "Exit", "action": lambda: self.switchContent("introScreen")}]

        # Create Puzzle Menu screen with all buttons
        self.puzzle_menu = Menu(
            object_name="puzzleMenu",
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="PUZZLE MENU",
            menu_buttons=puzzle_menu_buttons,
            bottom_buttons=puzzle_menu_bottom_buttons)
        return self.puzzle_menu

    def createToolMenu(self):
        # Create button list for Tool Menu
        tool_menu_buttons = [
            {"id": "btn1", "lbl": "Tool 1", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn2", "lbl": "Tool 2", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn3", "lbl": "Tool 3", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn4", "lbl": "Tool 4", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn5", "lbl": "Tool 5", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn6", "lbl": "Tool 6", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn7", "lbl": "Toole 7", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn8", "lbl": "Tool 8", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn9", "lbl": "PTool 9", "action": lambda: self.switchContent("loginScreen")}]

        # Create button list for bottom buttons
        tool_menu_bottom_buttons = [
            {"id": "back", "lbl": "Back", "action": lambda: self.switchContent("mainMenu")},
            {"id": "exit", "lbl": "Exit", "action": lambda: self.switchContent("introScreen")}]

        # Create Tool Menu screen with all buttons
        self.tool_menu = Menu(
            object_name="toolMenu",
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="TOOL MENU",
            menu_buttons=tool_menu_buttons,
            bottom_buttons=tool_menu_bottom_buttons)
        return self.tool_menu

    def createMediaMenu(self):
        # Create button list for Media Menu
        media_menu_buttons = [
            {"id": "btn1", "lbl": "Media 1", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn2", "lbl": "Media 2", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn3", "lbl": "Media 3", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn4", "lbl": "Media 4", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn5", "lbl": "Media 5", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn6", "lbl": "Media 6", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn7", "lbl": "Media 7", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn8", "lbl": "Media 8", "action": lambda: self.switchContent("loginScreen")},
            {"id": "btn9", "lbl": "Media 9", "action": lambda: self.switchContent("loginScreen")}]

        # Create button list for bottom buttons
        media_menu_bottom_buttons = [
            {"id": "back", "lbl": "Back", "action": lambda: self.switchContent("mainMenu")},
            {"id": "exit", "lbl": "Exit", "action": lambda: self.switchContent("introScreen")}]

        # Create Media Menu screen with all buttons
        self.media_menu = Menu(
            object_name="mediaMenu",
            header_label="Mr Robot",
            title_label="#FSOCIETY",
            splash_label="MEDIA MENU",
            menu_buttons=media_menu_buttons,
            bottom_buttons=media_menu_bottom_buttons)
        return self.media_menu

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

        if page == "emptyScreen":
            from gui.emptyScreen import EmptyScreen
            # Create empty screen content widget and connect signals to slots
            self.empty_screen = EmptyScreen(
                self, screen_dimensions=self.screen_dimensions)
            self.content.addWidget(self.empty_screen)
            self.empty_screen.exit.connect(
                lambda: self.switchContent("mainMenu"))

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
