'''
Program Name: Standard QT Framework

Program Description:
This is a basic QT framework which can be used to create a new program.
This program is currently in development.

File: topMenu.py
Function: Top menu Class

Author: Mario Kuijpers
Version: 1.0
Created: 01-06-2024
Last Updated: 24-07-2024

'''

# Imports
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
