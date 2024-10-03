# ___________________________________________________________________
#   ___     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: gui\pygameWidget.py
# INFO: Pygame Widget for Portable Escape Game in a briefcase
#
# Author: Mario Kuijpers
# Start date: 30-09-2024
# Last update: 02-10-2024
# Github: https://github.com/M4R1N447/Escape-Game-Briefcase
# Status: In Progress
# ___________________________________________________________________

# Imports
import os
import random
import pygame
from pygame.locals import FULLSCREEN
#from Sound_class import Sound as Sound

# For Stand Alone set System Path as below
import sys
sys.path.append("P:/game/Briefcase Pi 3B/")

# Import Qt Modules
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPainter, QColor

# Custom Imports
from gui.widgets.headerWidget import HeaderWidget as Header

from config import FONT_PATH as FONT_PATH
from config import MEMORY_IMAGES_PATH as MEMORY_IMAGES_PATH

# Colors
from config import BRIEFCASE_BG_COLOR as BRIEFCASE_BG_COLOR
from config import STANDARD_FONT_COLOR as STANDARD_FONT_COLOR
from config import TITLE_FONT_COLOR as TITLE_FONT_COLOR
from config import BG_COLOR as BG_COLOR
from config import BG_LIGHT_COLOR as BG_LIGHT_COLOR
from config import RED as RED

# Fonts
from config import HEADER_FONT as HEADER_FONT
from config import SUBTITLE_FONT as SUBTITLE_FONT
from config import MAIN_FONT as MAIN_FONT

# Font Sizes
from config import HEADER_FONT_SIZE as HEADER_FONT_SIZE
from config import TITLE_FONT_SIZE as TITLE_FONT_SIZE

# Images
# from config import MEMORY_BG as MEMORY_BG

# Sounds
from config import ENIGMA_MEDIUM_CLK_SND as CLICK_SND


class Memory(QWidget):
    '''
    Pygame Widget
    '''
    def __init__(self,
                 main_window,
                 screen_dimensions,
                 object_name="memory",
                 width=1000,
                 height=600,
                 top_margin=100,
                 fps=60,
                 max_score=0,
                 difficulty=1,
                 complexity=None,
                 game_input=None,
                 hints=None,
                 solution=None):
        super().__init__()

        self.main_window = main_window
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.object_name = object_name
        self.width = width
        self.height = height
        self.top_margin = top_margin
        self.fps = fps

        self.max_score = max_score
        self.difficulty = difficulty
        self.complexity = complexity
        self.game_input = game_input
        self.hints = hints
        self.solution = solution

        # Set object name
        self.setObjectName(self.object_name)

        # Play Game
        self.Play()

    # Game Intro Screen
    def game_intro_screen(self):
        print()
        print("--------------------------------------------")
        print("           M E M O R Y   G A M E            ")
        print()
        print("Max Score = " + str(self.max_score*self.difficulty))
        print("Solution = " + str(self.solution) + " (for debugging)")
        print("--------------------------------------------")
        print()

    # Set Game Hints
    def game_hints(self):
        if self.difficulty == 1:
            self.hints = []
        elif self.difficulty == 2:
            self.hints = []
        elif self.difficulty == 3:
            self.hints = []
        return self.hints

    def Play(self):
        '''
        Initialize Pygame and create Pygame window
        '''

        # Initialize Pygame
        pygame.init()

        # Sound objects
        pygame.mixer.init()
        # game_music = Sound(file=GAME_AUDIO, volume=0.2, fade_in=0, fade_out=1000)
        # click_snd = Sound(CLICK_SND, 0.6, 0, 0)

        # Screen Width & Height
        # screeninfo = pygame.display.Info()
        # self.screen_w = screeninfo.current_w
        # self.screen_h = screeninfo.current_h

        # print("Screen Width: ", self.screen_w)
        # print("Screen Height: ", self.screen_h)

        # # Fullscreen without menu and borders
        # self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), FULLSCREEN)

        self.screen_w = self.screen_width
        self.screen_h = self.screen_height

        # Create a Pygame window
        self.screen = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        self.running = True

        # Create list of Memory Pictures
        memory_pictures = []

        # Convert fps to milliseconds and create timer to update Pygame screen
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePygame(memory_pictures))
        self.timer.start(int(1000 / self.fps))

        # Determine starting position of the game area
        self.x_pos = (((self.screen_width - self.width) // 2))
        self.y_pos = (((self.screen_height - self.height) // 2) + self.top_margin)

        # Determine game area dimensions
        self.game_width = self.x_pos + self.width
        self.game_height = self.y_pos + self.height

        # Variables
        self.pic_size = 128
        self.picture_columns = 5
        self.picture_rows = 4
        self.padding = 10
        self.picture_hide_delay = 1000  # (in msec)
        self.exit_game_delay = 5000  # (in msec)
        self.left_margin = ((self.screen_w - ((self.pic_size + self.padding) * self.picture_columns)) // 2)
        self.top_margin = (((self.screen_h - ((self.pic_size + self.padding) + self.picture_rows)) // 2) - 200)
        self.selection1 = None
        self.selection2 = None

        # Fonts
        self.header_font = pygame.font.Font((FONT_PATH + HEADER_FONT + ".ttf"), HEADER_FONT_SIZE + 30)
        self.title_font = pygame.font.Font((FONT_PATH + SUBTITLE_FONT + ".ttf"), TITLE_FONT_SIZE - 10)
        main_font = pygame.font.Font((FONT_PATH + MAIN_FONT + ".ttf"), 40)
        code_font = pygame.font.Font((FONT_PATH + MAIN_FONT + ".ttf"), 60)

        # Load background image
        self.screen.fill(BRIEFCASE_BG_COLOR)

        # Game Won Text
        self.game_won_text = "Good Work! You have found a secret code!"
        self.game_won_render = (main_font.render(self.game_won_text, True, (STANDARD_FONT_COLOR)))

        # Game Won Text Location
        self.game_won_rect = (self.game_won_render.get_rect(center=(self.screen_w/2, (self.screen_h/2)-150)))

        # Game Completed
        self.exit_code_text = "UNLOCKED CODE: "
        self.exit_code_render = (code_font.render(self.exit_code_text + str(self.solution), True, (STANDARD_FONT_COLOR)))

        # When game complete set player solution to game solution
        self.player_solution = self.solution

        # Game Completed Generated Code Text Location
        self.exit_code_rect = self.exit_code_render.get_rect(center=(self.screen_w/2, (self.screen_h/2)))

        # For different picture sets set this to another folder with 10 pictures in it
        set = "set_1/"

        # List all files in memory dir
        for item in os.listdir(str(MEMORY_IMAGES_PATH) + str(set)):
            # Add items without extention to list (Split at .)
            memory_pictures.append(item.split('.')[0])

        # Copy the list of images to a second list (We need 2 images of each)
        memory_pictures_copy = memory_pictures.copy()

        # Now we need to extend the list with the copies
        memory_pictures.extend(memory_pictures_copy)

        # The copied list can now be cleared
        memory_pictures_copy.clear()

        # Shuffle the list items
        random.shuffle(memory_pictures)

        # Create empty lists
        self.mem_pics = []
        self.mem_pics_rect = []
        self.hidden_images = []

        # Load each image in python memory
        for item in memory_pictures:
            # Get filename
            picture = pygame.image.load(MEMORY_IMAGES_PATH + set + f'{item}.jpg')

            # Resize picture to tile
            picture = pygame.transform.scale(picture, (self.pic_size, self.pic_size))

            # Append picture to mem_pics list
            self.mem_pics.append(picture)

            # Append picture_rect to mem_pics_rect list
            picture_rect = picture.get_rect()
            self.mem_pics_rect.append(picture_rect)

        for i in range(len(self.mem_pics_rect)):
            self.mem_pics_rect[i][0] = (self.left_margin + ((self.pic_size + self.padding) * (i % self.picture_columns)))
            self.mem_pics_rect[i][1] = (self.top_margin + ((self.pic_size + self.padding) * (i % self.picture_rows)))
            self.hidden_images.append(False)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Push header to top
        layout.addStretch()

        # Set layout
        self.setLayout(layout)

    def updatePygame(self, memory_pictures):
        '''
        Update Pygame screen
        '''
        if self.running:

            # Check for Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen with transparent black
            self.screen.fill((0, 0, 0, 0))

            # Draw border around game area
            pygame.draw.rect(
                self.screen, (0, 90, 0),
                (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4))

            # Draw background of game area
            pygame.draw.rect(
                self.screen, (50, 50, 50),
                (self.x_pos, self.y_pos, self.width, self.height))

            # Header
            header_text = self.header_font.render("Mr. ROBOT", True, RED)
            header_rect = header_text.get_rect(center=(self.screen_w/2, 80))
            self.screen.blit(header_text, header_rect)

            # Title
            title_text = self.title_font.render("- HACK YOUR MEMORY -", True, TITLE_FONT_COLOR)
            title_rect = title_text.get_rect(center=(self.screen_w/2, 180))
            self.screen.blit(title_text, title_rect)

            # Input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Detect a mousclick
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Play mouseclick sound
                    # click_snd.play_sound()

                    for item in self.mem_pics_rect:

                        # Check if mouse position is on a picture
                        if item.collidepoint(event.pos):
                            if not self.hidden_images[self.mem_pics_rect.index(item)]:
                                if selection1 is not None:
                                    selection2 = self.mem_pics_rect.index(item)

                                    # Show picture
                                    self.hidden_images[selection2] = True
                                else:
                                    selection1 = self.mem_pics_rect.index(item)
                                    # Show picture
                                    self.hidden_images[selection1] = True

                # Detect a keypress
                if event.type == pygame.KEYDOWN:
                    # Play keypress sound
                    # click_snd.play_sound()

                    # Exit when Escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            for i in range(len(memory_pictures)):
                if self.hidden_images[i] is True:
                    # Show image
                    self.screen.blit(self.mem_pics[i], self.mem_pics_rect[i])
                    # Draw a border around images
                    pygame.draw.rect(self.screen, STANDARD_FONT_COLOR,
                                     (self.mem_pics_rect[i][0], self.mem_pics_rect[i][1],
                                      self.pic_size, self.pic_size), 1)
                else:
                    # Hide image
                    pygame.draw.rect(self.screen, BG_COLOR,
                                     (self.mem_pics_rect[i][0], self.mem_pics_rect[i][1],
                                      self.pic_size, self.pic_size))
                    pygame.draw.rect(self.screen, BG_LIGHT_COLOR,
                                     (self.mem_pics_rect[i][0], self.mem_pics_rect[i][1],
                                      self.pic_size, self.pic_size), 1)

            pygame.display.update()

            if selection1 is not None and selection2 is not None:
                # Check if clicked pictues match
                if memory_pictures[selection1] == memory_pictures[selection2]:
                    selection1, selection2 = None, None
                else:
                    # Make pictures hidden again
                    pygame.time.wait(self.picture_hide_delay)
                    self.hidden_images[selection1] = False
                    self.hidden_images[selection2] = False
                    selection1, selection2 = None, None

            # Check if the game is won
            win = 1
            for number in range(len(self.hidden_images)):
                # Win * Image If all are 1 then 1*1 else 1*0 win = 0
                win *= self.hidden_images[number]

            if win == 1:
                # Screen when game is won
                self.screen.fill(BRIEFCASE_BG_COLOR, (0, 0, self.screen_w, self.screen_h))
                # screen.blit(bg_image, bg_image_rect)

                # Header
                header_text = self.header_font.render("Mr. ROBOT", True, RED)
                header_rect = header_text.get_rect(center=(self.screen_w/2, 80))
                self.screen.blit(header_text, header_rect)

                # Title
                title_text = self.title_font.render("- HACK YOUR MEMORY -", True, TITLE_FONT_COLOR)
                title_rect = title_text.get_rect(center=(self.screen_w/2, 180))
                self.screen.blit(title_text, title_rect)

                self.screen.blit(self.game_won_render, self.game_won_rect)
                self.screen.blit(self.exit_code_render, self.exit_code_rect)
                pygame.display.update()
                pygame.time.wait(self.exit_game_delay)
                self.running = False

            pygame.display.update()

            # pygame.display.quit()
            pygame.display.flip()

            # Close window and go back to menu
            pygame.display.quit()

            # After game go back to Puzzle Data Class
            return self.player_solution

        self.repaint()

    def paintEvent(self, event):
        '''
        Paint event for Pygame screen
        '''
        if self.running:
            q_image = self.convertPygameSurfaceToQImage(self.window)
            painter = QPainter(self)
            painter.drawImage(0, 0, q_image)

    def convertPygameSurfaceToQImage(self, surface):
        ''' Convert Pygame surface to QImage '''
        width, height = surface.get_size()
        data = surface.get_buffer().raw
        q_image = QImage(data, width, height, QImage.Format.Format_ARGB32)
        return q_image

    def closeEvent(self, event):
        ''' Close event for Pygame screen '''
        self.running = False
        pygame.quit()
        event.accept()
