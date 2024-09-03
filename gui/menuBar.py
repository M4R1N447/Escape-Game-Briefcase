# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\menuBar.py
# INFO: Top menu bar for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 01-06-2024
# Last update: 03-09-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________


# Import Qt Modules
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal


class MenuBar(QMenuBar):
    '''
    Top Menu Class
    '''

    # Define signals which can be emitted to the main window
    exit = pyqtSignal()
    intro = pyqtSignal()
    login = pyqtSignal()
    mainMenu = pyqtSignal()
    puzzleMenu = pyqtSignal()
    toolMenu = pyqtSignal()
    mediaMenu = pyqtSignal()
    page2 = pyqtSignal()
    page3 = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Create File menu with Exit action
        file_menu = QMenu("File", self)
        exit = QAction("Exit", self)
        exit.triggered.connect(lambda: self.exit.emit())
        file_menu.addAction(exit)
        self.addMenu(file_menu)

        # Create Pages menu with some example pages
        page_menu = QMenu("Pages", self)

        intro = QAction("Intro Screen", self)
        intro.triggered.connect(lambda: self.intro.emit())
        page_menu.addAction(intro)

        login = QAction("Login Screen", self)
        login.triggered.connect(lambda: self.login.emit())
        page_menu.addAction(login)

        menu = QAction("Main Menu", self)
        menu.triggered.connect(lambda: self.mainMenu.emit())
        page_menu.addAction(menu)

        menu = QAction("Puzzle Menu", self)
        menu.triggered.connect(lambda: self.puzzleMenu.emit())
        page_menu.addAction(menu)

        menu = QAction("Tool Menu", self)
        menu.triggered.connect(lambda: self.toolMenu.emit())
        page_menu.addAction(menu)

        menu = QAction("Media Menu", self)
        menu.triggered.connect(lambda: self.mediaMenu.emit())
        page_menu.addAction(menu)

        page2 = QAction("Page 2", self)
        page2.triggered.connect(lambda: self.page2.emit())
        page_menu.addAction(page2)

        page3 = QAction("Page 3", self)
        page3.triggered.connect(lambda: self.page3.emit())
        page_menu.addAction(page3)
        self.addMenu(page_menu)

        # Create View menu with some example actions
        view_menu = QMenu("View", self)
        example_action1 = QAction("Example 1", self)
        view_menu.addAction(example_action1)
        example_action2 = QAction("Example 2", self)
        view_menu.addAction(example_action2)
        self.addMenu(view_menu)
