# __________________________________________________
# FILE: game/Briefcase Pi 3B/Periodic_Table/periodic_table.py
# INFO: Periodic Table Tool for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 10-08-2023
# Last update: 11-08-2023
# Github: https://github.com/M4R1N447/Mr.-Robot-Escape-Game-Briefcase
# Status: In Progress
# __________________________________________________

# Imports
import os
import random
from Sound_class import Sound as Sound
import pygame
from pygame.locals import FULLSCREEN


#
# VARIABLES IMPORTED FROM CONFIG FILE
# __________________________________________________

# Paths
from config import FONT_PATH as FONT_PATH
from config import MEMORY_IMAGES_PATH as MEMORY_IMAGES_PATH

# Colors
from config import BRIEFCASE_BG_COLOR as BRIEFCASE_BG_COLOR
from config import STANDARD_FONT_COLOR as STANDARD_FONT_COLOR
from config import BG_COLOR as BG_COLOR
from config import BG_LIGHT_COLOR as BG_LIGHT_COLOR

# Fonts
from config import HEADER_FONT as HEADER_FONT
from config import MAIN_FONT as MAIN_FONT

# Images
from config import MEMORY_BG as MEMORY_BG

# Game Class
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
        print("   P E R I O D I C   T A B L E   T O O L    ")
        print()
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


        # GUI with periodic table

        import pygame

        from clean_csv import scrub_the_csv as scrub

        pygame.init()

        # - S O U N D S   A N D   M U S I C - #

        # Sound objects
        pygame.mixer.init()
        # game_music = Sound(file=GAME_AUDIO, volume=0.2, fade_in=0, fade_out=1000)

        # each element in order of name, atomic num, symbol, weight, col, row
        dataset = scrub()

        fps = 60
        WIDTH = 800
        HEIGHT = 600

        screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Periodic Table")
        timer = pygame.time.Clock()

        font = pygame.font.Font('freesansbold.ttf', 16)
        midfont = pygame.font.Font('freesansbold.ttf', 28)
        bigfont = pygame.font.Font('freesansbold.ttf', 36)

        cols = 18
        rows = 10

        cell_width = WIDTH / cols
        cell_height = HEIGHT / rows

        highlight = False

        colors = [("Alkali Metals", "light blue"),
                ("Metalloids", "yellow"),
                ("Actinides", "orange"),
                ("Alkaline Earth Metals", "red"),
                ("Reactive Nonmetals", "blue"),
                ("Unknown Properties", "dark gray"),
                ("Transition Metals", "purple"),
                ("Post-Transition Metals", "green"),
                ("Noble Gases", "dark red"),
                ("Lanthanides", "light gray")]

        groups = [[3, 11, 19, 37, 55, 87],
                [5, 14, 32, 33, 51, 52],
                [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103],
                [4, 12, 20, 38, 56, 88],
                [1, 6, 7, 8, 9, 15, 16, 17, 34, 35, 53],
                [109, 110, 111, 112, 113, 114, 115, 116, 117, 118],
                [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44,
                45, 46, 47, 48, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                104, 105, 106, 107, 108],
                [13, 31, 49, 50, 81, 82, 83, 84, 85],
                [2, 10, 18, 36, 54, 86],
                [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]]

        def draw_screen(data):
            element_list = []

            # for each element in this data
            for i in range(len(data)):

                # name, number, symbol, weight, col, row
                elem = data[i]

                # for each group
                for q in range(len(groups)):

                    # if atomic number is in this group
                    if int(elem[1]) in groups[q]:
                        
                        # Get the color for this element
                        color = colors[q][1]

                # COLUMN
                if elem[4] < 3:
                    x_pos = (elem[4] - 1) * cell_width
                else:
                    x_pos = (elem[4] - 2) * cell_width

                # ROW
                y_pos = (elem[5] - 2) * cell_height

                # manually move 2 elements
                if elem[4] == 4 and elem[5] in [7,8]:
                    x_pos = (elem[4] + 12) * cell_width
                    y_pos = (elem[5] + 1) * cell_height

                # element
                box = pygame.draw.rect(screen, color,
                                    [x_pos, y_pos, cell_width - 4, cell_height - 4])
                pygame.draw.rect(screen, "silver",
                                [x_pos - 2, y_pos - 2, cell_width, cell_height], 2)
                
                # Draw atomic number
                screen.blit(font.render(elem[1], True, "black"), (x_pos + 5, y_pos + 5))

                # Draw symbol
                screen.blit(font.render(elem[2], True, "black"), (x_pos + 5, y_pos + 20))

                element_list.append((box, (i, color)))

                # lanths and acts explainers
                pygame.draw.rect(screen, "white",
                                [cell_width * 2 - 3, cell_height * 5 - 3, cell_width, 2 * cell_height], 3, 5)
                pygame.draw.rect(screen, "white",
                                [cell_width * 2 - 3, cell_height * 8 - 3, cell_width * 15, 2 * cell_height], 3, 5)
                pygame.draw.line(screen, "white", (cell_width * 2 - 3, cell_height * 6), (cell_width * 2 - 3, cell_height * 9), 3)

            return element_list

        def draw_highlight(info):
            classification = ""
            information = dataset[info[0]]

            # from this element check the color and get that classification
            for i in range(len(colors)):
                if colors[i][1] == info[1]:
                    classification = colors[i][0]

            # draw a filled rectangle with radius 5
            pygame.draw.rect(screen, "light gray", [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 0, 5)
            pygame.draw.rect(screen, "black", [cell_width * 3, cell_height * 1.5, cell_width * 8, cell_height * 0.8], 0, 5)
            pygame.draw.rect(screen, "dark gray", [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 8, 5)
            pygame.draw.rect(screen, info[1], [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 5, 5)

            screen.blit(bigfont.render(information[1] + '-' + information[2], True, "black"), (cell_width * 3 + 5, cell_height * 0.5 + 10))
            screen.blit(midfont.render(information[0], True, "black"), (cell_width * 6 + 10, cell_height * 0.5 + 10))
            screen.blit(midfont.render(information[3], True, "black"), (cell_width * 6 + 10, cell_height * 0.9 + 10))
            screen.blit(midfont.render(classification, True, info[1]), (cell_width * 3 + 10, cell_height * 1.5 + 10))



        run = True
        while run:
            screen.fill("black")
            timer.tick(fps)
            elements = draw_screen(dataset)

            if highlight:
                draw_highlight(info)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # get mouse position
            mouse_pos = pygame.mouse.get_pos()
            highlight = False
            
            # for each element
            for e in range(len(elements)):
                
                # if the mouse collides with the box of an element
                if elements[e][0].collidepoint(mouse_pos):
                    highlight = True
                    
                    # info = index and color of the element
                    info = elements[e][1]

            pygame.display.flip()
        pygame.quit()
