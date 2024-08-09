'''
Program Name: Standard QT Framework

Program Description:
This is a basic QT framework which can be used to create a new program.
This program is currently in development.

File: functions.py
Function: Standalone functions which can be used in program

Author: Mario Kuijpers
Version: 1.0
Created: 01-06-2024
Last Updated: 24-07-2024

'''

# Imports
import os


def createPath(relative_path):
    """
    Create an absolute path from a relative path name
    Example: path = create_path("src/gui") gives: C:/Data/Python/RFPro/src/gui/
    """

    # Get absolute path
    absolute_path = os.path.dirname(__file__)

    # Check if absolute path and relative path are the same
    if "gui" in absolute_path and "gui" in relative_path:
        created_path = os.path.join(f"{absolute_path}\\")
    else:
        # Create path from relative path name and add '\' at end of path
        created_path = os.path.join(f"{absolute_path}\\{relative_path}\\")
    return created_path
