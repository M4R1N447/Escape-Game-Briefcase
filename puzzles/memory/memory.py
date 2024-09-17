# __________________________________________________
# FILE: game/Briefcase Pi 3B/Memory/memory.py
# INFO: Memory puzzle for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 17-02-2022
# Last update: 08-11-2022
# Github: https://github.com/M4R1N447/Mr.-Robot-Escape-Game-Briefcase
# Status: In Progress
# __________________________________________________

# Imports
import os
import random
import pygame
from pygame.locals import FULLSCREEN
#from Sound_class import Sound as Sound

# For Stand Alone set System Path as below
import sys
sys.path.append("P:/game/Briefcase Pi 3B/")

#
# VARIABLES IMPORTED FROM CONFIG FILE
# __________________________________________________


# Paths
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


# Memory
class Game:
    def __init__(self, max_score=0, difficulty=1, complexity=None,
                 game_input=None, hints=None, solution=None):
        self.max_score = max_score
        self.difficulty = difficulty
        self.complexity = complexity
        self.game_input = game_input
        self.hints = hints
        self.solution = solution

    # Get Max Score from Puzzle_data Class
    def set_max_score(self, max_score):
        self.max_score = max_score

    # Get game difficulty from Puzzle_data Class
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    # Get game difficulty from Puzzle_data Class
    def set_complexity(self, complexity):
        self.complexity = complexity

    def set_game_input(self, game_input):
        self.game_input = game_input

    # Get game difficulty from Puzzle_data Class
    def set_solution(self, solution):
        self.solution = solution

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

    # Main Game
    def game_play(self):

        print("Memory Game Started...") 
        # Initialize Pygame
        pygame.init()
        
        # - S O U N D S   A N D   M U S I C - #

        # Sound objects
        pygame.mixer.init()
        # game_music = Sound(file=GAME_AUDIO, volume=0.2, fade_in=0, fade_out=1000)
        #click_snd = Sound(CLICK_SND, 0.6, 0, 0)

        # Screen Width & Height
        screeninfo = pygame.display.Info()
        screen_w = screeninfo.current_w
        screen_h = screeninfo.current_h

        # Fullscreen without menu and borders
        screen = pygame.display.set_mode((screen_w, screen_h), FULLSCREEN)

        # Variables
        pic_size = 128
        picture_columns = 5
        picture_rows = 4
        padding = 10
        picture_hide_delay = 1000  # (in msec)
        exit_game_delay = 5000  # (in msec)
        left_margin = ((screen_w - ((pic_size + padding) *
                       picture_columns)) // 2)
        top_margin = (((screen_h - ((pic_size + padding) +
                      picture_rows)) // 2) - 200)
        selection1 = None
        selection2 = None

        # Fonts
        header_font = pygame.font.Font((FONT_PATH + HEADER_FONT + ".ttf"), HEADER_FONT_SIZE + 30)
        title_font = pygame.font.Font((FONT_PATH + SUBTITLE_FONT + ".ttf"), TITLE_FONT_SIZE - 10)
        main_font = pygame.font.Font((FONT_PATH + MAIN_FONT + ".ttf"), 40)
        code_font = pygame.font.Font((FONT_PATH + MAIN_FONT + ".ttf"), 60)

        # Load background image
        screen.fill(BRIEFCASE_BG_COLOR)
        # bg_image = pygame.image.load(MEMORY_BG)

        # Resize image
        # bg_image = pygame.transform.scale(bg_image, (screen_w, screen_h))
        # bg_image_rect = bg_image.get_rect()

        # Screen Title
        # title_text = "HACK YOUR MEMORY"
        # title_render = (title_font.render(title_text, True,
        #                 (STANDARD_FONT_COLOR)))
        # # Screen Title Location
        # title_rect = title_render.get_rect(center=(screen_w/2, 50))

        # Game Won Text
        game_won_text = "Good Work! You have found a secret code!"
        game_won_render = (main_font.render(game_won_text, True,
                           (STANDARD_FONT_COLOR)))
        # Game Won Text Location
        game_won_rect = (game_won_render.get_rect(center=(screen_w/2,
                         (screen_h/2)-150)))

        # Game Completed
        exit_code_text = "UNLOCKED CODE: "
        exit_code_render = (code_font.render(exit_code_text +
                            str(self.solution), True, (STANDARD_FONT_COLOR)))
        # When game complete set player solution to game solution
        self.player_solution = self.solution
        # Game Completed Generated Code Text Location
        exit_code_rect = exit_code_render.get_rect(center=(screen_w/2,
                                                           (screen_h/2)))

        # Create list of Memory Pictures
        memory_pictures = []

        # For different picture sets set this to another folder with 10 pictures in it
        set = "set_1/"

        # List all files in memory dir
        for item in os.listdir(MEMORY_IMAGES_PATH + set):
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
        mem_pics = []
        mem_pics_rect = []
        hidden_images = []

        # Load each image in python memory
        for item in memory_pictures:
            # Get filename
            picture = pygame.image.load(MEMORY_IMAGES_PATH + set +f'{item}.jpg')

            # Resize picture to tile
            picture = pygame.transform.scale(picture, (pic_size, pic_size))

            # Append picture to mem_pics list
            mem_pics.append(picture)

            # Append picture_rect to mem_pics_rect list
            picture_rect = picture.get_rect()
            mem_pics_rect.append(picture_rect)

        for i in range(len(mem_pics_rect)):
            mem_pics_rect[i][0] = (left_margin + ((pic_size + padding) *
                                   (i % picture_columns)))
            mem_pics_rect[i][1] = (top_margin + ((pic_size + padding) *
                                   (i % picture_rows)))
            hidden_images.append(False)

        game_loop = True
        while game_loop:
            # Load background image
            # screen.blit(bg_image, bg_image_rect)

            # Header
            header_text = header_font.render("Mr. ROBOT", True, RED)
            header_rect = header_text.get_rect(center=(screen_w/2, 80))
            screen.blit(header_text, header_rect)

            # Title
            title_text = title_font.render("- HACK YOUR MEMORY -", True, TITLE_FONT_COLOR)
            title_rect = title_text.get_rect(center=(screen_w/2, 180))
            screen.blit(title_text, title_rect)

            # Input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False

                # Detect a mousclick
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Play mouseclick sound
                    # click_snd.play_sound()

                    for item in mem_pics_rect:

                        # Check if mouse position is on a picture
                        if item.collidepoint(event.pos):
                            if not hidden_images[mem_pics_rect.index(item)]:
                                if selection1 is not None:
                                    selection2 = mem_pics_rect.index(item)

                                    # Show picture
                                    hidden_images[selection2] = True
                                else:
                                    selection1 = mem_pics_rect.index(item)
                                    # Show picture
                                    hidden_images[selection1] = True

                # Detect a keypress
                if event.type == pygame.KEYDOWN:
                    # Play keypress sound
                    click_snd.play_sound()

                    # Exit when Escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        game_loop = False

            for i in range(len(memory_pictures)):
                if hidden_images[i] is True:
                    # Show image
                    screen.blit(mem_pics[i], mem_pics_rect[i])
                    # Draw a border around images
                    pygame.draw.rect(screen, STANDARD_FONT_COLOR,
                                     (mem_pics_rect[i][0], mem_pics_rect[i][1],
                                      pic_size, pic_size), 1)
                else:
                    # Hide image
                    pygame.draw.rect(screen, BG_COLOR,
                                     (mem_pics_rect[i][0], mem_pics_rect[i][1],
                                      pic_size, pic_size))
                    pygame.draw.rect(screen, BG_LIGHT_COLOR,
                                     (mem_pics_rect[i][0], mem_pics_rect[i][1],
                                      pic_size, pic_size), 1)

            pygame.display.update()

            if selection1 is not None and selection2 is not None:
                # Check if clicked pictues match
                if memory_pictures[selection1] == memory_pictures[selection2]:
                    selection1, selection2 = None, None
                else:
                    # Make pictures hidden again
                    pygame.time.wait(picture_hide_delay)
                    hidden_images[selection1] = False
                    hidden_images[selection2] = False
                    selection1, selection2 = None, None

            # Check if the game is won
            win = 1
            for number in range(len(hidden_images)):
                # Win * Image If all are 1 then 1*1 else 1*0 win = 0
                win *= hidden_images[number]

            if win == 1:
                # Screen when game is won
                screen.fill(BRIEFCASE_BG_COLOR, (0, 0, screen_w, screen_h))
                # screen.blit(bg_image, bg_image_rect)

                # Header
                header_text = header_font.render("Mr. ROBOT", True, RED)
                header_rect = header_text.get_rect(center=(screen_w/2, 80))
                screen.blit(header_text, header_rect)

                # Title
                title_text = title_font.render("- HACK YOUR MEMORY -", True, TITLE_FONT_COLOR)
                title_rect = title_text.get_rect(center=(screen_w/2, 180))
                screen.blit(title_text, title_rect)

                screen.blit(game_won_render, game_won_rect)
                screen.blit(exit_code_render, exit_code_rect)
                pygame.display.update()
                pygame.time.wait(exit_game_delay)
                game_loop = False

            pygame.display.update()

        # pygame.display.quit()
        pygame.display.flip()

        # Close window and go back to menu
        pygame.display.quit()

        # After game go back to Puzzle Data Class
        return self.player_solution
