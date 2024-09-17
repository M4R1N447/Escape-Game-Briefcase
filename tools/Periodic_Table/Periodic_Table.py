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
import pygame
from pygame.locals import FULLSCREEN
from clean_csv import scrub_the_csv as scrub
from Sound_class import Sound as Sound

#
# VARIABLES IMPORTED FROM CONFIG FILE
# __________________________________________________

# Paths
from config import FONT_PATH as FONT_PATH

# Colors
from config import BRIEFCASE_BG_COLOR as BRIEFCASE_BG_COLOR
from config import STANDARD_FONT_COLOR as STANDARD_FONT_COLOR
from config import TITLE_FONT_COLOR as TITLE_FONT_COLOR
from config import BG_COLOR as BG_COLOR
from config import BG_LIGHT_COLOR as BG_LIGHT_COLOR
from config import BG_DARK_COLOR as BG_DARK_COLOR
from config import EXTRA_DARK_PURPLE as EXTRA_DARK_PURPLE
from config import LIGHT_BLUE as LIGHT_BLUE
from config import YELLOW as YELLOW
from config import ORANGE as ORANGE
from config import LIGHT_RED as LIGHT_RED
from config import MEDIUM_RED as MEDIUM_RED
from config import RED as RED
from config import LIGHT_GRAY as LIGHT_GRAY
from config import GRAY as GRAY
from config import PURPLE as PURPLE
from config import GREEN as GREEN
from config import LIGHT_PINK as LIGHT_PINK
from config import LIGHT_YELLOW as LIGHT_YELLOW
from config import EXTRA_LIGHT_ORANGE as EXTRA_LIGHT_ORANGE

# Fonts
from config import STANDARD_FONT as STANDARD_FONT
from config import MAIN_FONT as MAIN_FONT
from config import HEADER_FONT as HEADER_FONT
from config import TITLE_FONT as TITLE_FONT
from config import SUBTITLE_FONT as SUBTITLE_FONT

# Fontsizes
from config import STANDARD_FONT_SIZE as STANDARD_FONT_SIZE
from config import MAIN_FONT_SIZE_BIG as MAIN_FONT_SIZE_BIG
from config import HEADER_FONT_SIZE as HEADER_FONT_SIZE
from config import TITLE_FONT_SIZE as TITLE_FONT_SIZE
from config import SUBTITLE_FONT_SIZE as SUBTITLE_FONT_SIZE

# Sounds
from config import ENIGMA_MEDIUM_CLK_SND as CLICK_SND

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
        # Initialize Pygame
        pygame.init()

        # Sound objects
        pygame.mixer.init()
        # game_music = Sound(file=GAME_AUDIO, volume=0.2, fade_in=0, fade_out=1000)
        click_snd = Sound(CLICK_SND, 0.6, 0, 0)

        # Get and Set Screen Width & Height
        screeninfo = pygame.display.Info()
        screen_w = screeninfo.current_w
        screen_h = screeninfo.current_h

        # Game window width and height
        game_width = 800
        game_height = 600

        # Calculate offset betweet full screen width and height and game width and height
        x_offset = (screen_w // 2) - (game_width // 2)
        y_offset = (screen_h // 2) - (game_height // 2) + 100

        # Fullscreen without menu and borders
        screen = pygame.display.set_mode((screen_w, screen_h), FULLSCREEN)
        pygame.display.set_caption("Periodic Table")

        fps = 60
        timer = pygame.time.Clock()

        # Fonts
        header_font = pygame.font.Font((FONT_PATH + HEADER_FONT + ".ttf"), HEADER_FONT_SIZE + 30)
        title_font = pygame.font.Font((FONT_PATH + SUBTITLE_FONT + ".ttf"), TITLE_FONT_SIZE - 10)

        font = pygame.font.Font('freesansbold.ttf', 18)
        midfont = pygame.font.Font('freesansbold.ttf', 28)
        bigfont = pygame.font.Font('freesansbold.ttf', 36)

        # Each element in order of name, atomic num, symbol, weight, col, row
        dataset = scrub()

        # Define number of rows and columns for elements
        cols = 18
        rows = 10

        cell_width = game_width // cols
        cell_height = game_height // rows

        highlight = False

        # Define colors for each element group
        colors = [("Alkali Metals", LIGHT_RED),
                ("Metalloids", LIGHT_BLUE),
                ("Actinides", ORANGE),
                ("Alkaline Earth Metals", EXTRA_LIGHT_ORANGE),
                ("Reactive Nonmetals", YELLOW),
                ("Unknown Properties", GRAY),
                ("Transition Metals", PURPLE),
                ("Post-Transition Metals", GREEN),
                ("Noble Gases", LIGHT_PINK),
                ("Lanthanides", LIGHT_YELLOW)]

        # Define which element belongs to which group
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
            color = "white"

            for i in range(len(data)):
                # name, number, symbol, weight, col, row
                elem = data[i]

                # For each group
                for q in range(len(groups)):

                    # if atomic number is in this group
                    if int(elem[1]) in groups[q]:
                        
                        # Get the color for this element
                        color = colors[q][1]

                # Draw COLUMNS
                if elem[4] < 3:
                    x_pos = (elem[4] - 1) * cell_width + x_offset
                else:
                    x_pos = (elem[4] - 2) * cell_width + x_offset

                # Draw ROWS
                y_pos = (elem[5] - 2) * cell_height + y_offset

                # Manually move 2 elements
                if elem[4] == 4 and elem[5] in [7,8]:
                    x_pos = (elem[4] + 12) * cell_width + x_offset
                    y_pos = (elem[5] + 1) * cell_height + y_offset

                # Element
                border = pygame.draw.rect(screen, color,
                                    [x_pos , y_pos, cell_width - 4, cell_height - 4])
                pygame.draw.rect(screen, BG_LIGHT_COLOR,
                                [x_pos - 2 , y_pos - 2, cell_width, cell_height], 2)
                
                # Draw atomic number
                screen.blit(font.render(elem[1], True, BG_DARK_COLOR), (x_pos + 5, y_pos + 5))

                # Draw symbol
                screen.blit(font.render(elem[2], True, BG_DARK_COLOR), (x_pos + 5, y_pos + 20))

                element_list.append((border, (i, color)))

                # lanths and acts explainers
                pygame.draw.rect(screen, BG_LIGHT_COLOR,
                                [cell_width * 2 - 2 + x_offset, cell_height * 5 - 2 + y_offset, cell_width, 2 * cell_height], 3, 5)
                pygame.draw.rect(screen, BG_LIGHT_COLOR,
                                [cell_width * 2 - 2 + x_offset, cell_height * 8 - 2  + y_offset, cell_width * 15, 2 * cell_height], 3, 5)
                pygame.draw.line(screen, BG_LIGHT_COLOR, (cell_width * 2 - 2 + x_offset, cell_height * 6 + y_offset), (cell_width * 2 - 2 + x_offset, cell_height * 10 - 5 + y_offset), 3)

            return element_list

        def draw_highlight(info):
            classification = ""
            information = dataset[info[0]]

            # from this element check the color and get that classification
            for i in range(len(colors)):
                if colors[i][1] == info[1]:
                    classification = colors[i][0]

            # draw a filled rectangle with radius 5
            pygame.draw.rect(screen, BG_LIGHT_COLOR, [cell_width * 3 + x_offset, cell_height * 0.5 + y_offset, cell_width * 8, cell_height * 2], 0, 5)
            pygame.draw.rect(screen, EXTRA_DARK_PURPLE, [cell_width * 3 + x_offset, cell_height * 1.5 + y_offset + 5, cell_width * 8, cell_height * 0.8], 0, 5)
            pygame.draw.rect(screen, EXTRA_DARK_PURPLE, [cell_width * 3 + x_offset, cell_height * 0.5 + y_offset, cell_width * 8, cell_height * 2], 8, 5)
            pygame.draw.rect(screen, info[1], [cell_width * 3 + x_offset, cell_height * 0.5 + y_offset, cell_width * 8, cell_height * 2], 5, 5)
            
            # 0 = name, 1 = number, 2 = symbol, 3 = weight
            screen.blit(bigfont.render(information[1] + '-' + information[2], True, STANDARD_FONT_COLOR), (cell_width * 3 + 8 + x_offset, cell_height * 0.5 + 10 + y_offset))
            screen.blit(midfont.render(information[0], True, STANDARD_FONT_COLOR), (cell_width * 6 + 8 + x_offset, cell_height * 0.5 + 10 + y_offset))
            screen.blit(midfont.render(information[3], True, STANDARD_FONT_COLOR), (cell_width * 6 + 8 + x_offset, cell_height * 0.9 + 10 + y_offset))
            screen.blit(midfont.render(classification, True, info[1]), (cell_width * 3 + 10 + x_offset, cell_height * 1.5 + 15 + y_offset))

        run = True

        # Main Loop
        while run:

            # Check events
            for event in pygame.event.get():
                # Window closed
                if event.type == pygame.QUIT:
                    run = False

                # Detect a keypress
                if event.type == pygame.KEYDOWN:
                    # Exit when Escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        run = False

            # Fill screen with background color
            screen.fill(BRIEFCASE_BG_COLOR)

            # Header
            header_text = header_font.render("Mr. ROBOT", True, RED)
            header_rect = header_text.get_rect(center=(screen_w/2, 80))
            screen.blit(header_text, header_rect)

            # Title
            title_text = title_font.render("- P E R I O D I C   T A B L E -", True, TITLE_FONT_COLOR)
            title_rect = title_text.get_rect(center=(screen_w/2, 180))
            screen.blit(title_text, title_rect)

            # Draw screen
            elements = draw_screen(dataset)

            if highlight:
                draw_highlight(info)

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
            
            # Set frames timer to fps
            timer.tick(fps)
            
            # Update display
            pygame.display.flip()
        
        # Quit pygame and return to main menu
        pygame.display.quit()
