# __________________________________________________
# FILE: game/Briefcase Pi 3B/Pacman/pacman.py
# INFO: Pacman Game for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 15-02-2023
# Last update: 17-03-2023
# Github: https://github.com/M4R1N447/Mr.-Robot-Escape-Game-Briefcase
# Status: In Progress
#
# Tutorial: https://www.youtube.com/watch?v=9H27CimgPsQ
# Github: https://github.com/plemaster01/PythonPacman
# __________________________________________________


# Imports
import pygame
from pygame import mixer
from pygame.locals import FULLSCREEN
from Sound_class import Sound as Sound

from boards import boards
import math
import copy

# For Stand Alone set System Path as below
# # import sys
# # sys.path.append("P:/game/Briefcase Pi 3B/")

#
# VARIABLES IMPORTED FROM CONFIG FILE
# __________________________________________________

# Paths
from config import PACMAN_PLAYER_IMG_PATH as PLAYER_IMG_PATH
from config import PACMAN_GHOST_IMG_PATH as GHOST_IMG_PATH
from config import PACMAN_SOUNDS_PATH as SOUNDS_PATH
from config import FONT_PATH as FONT_PATH

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
        print("           P A C M A N    G A M E           ")
        print()
        print("Max Score = " + str(self.max_score * self.difficulty))
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

        # Initialize Variables
        # SCREEN SETTINGS
        WIDTH = 900
        HEIGHT = 950

        # Calculate offset betweet full screen width and height and game width and height
        x_offset = (screen_w // 2) - (WIDTH // 2)
        y_offset = (screen_h // 2) - (HEIGHT // 2)

        # Math variable
        PI = math.pi

        # Colors
        background_color = "black"
        text_color = "white"
        small_dot_color = "white"
        big_dot_color = "green"
        line_color = "blue"
        door_color = "white"

        # Determine which board to be loaded and copy it for this level
        level = copy.deepcopy(boards)

        # Initialize Screen Display Width & Height
        # screen = pygame.display.set_mode([WIDTH, HEIGHT], FULLSCREEN)
        screen = pygame.display.set_mode([screen_w, screen_h], FULLSCREEN)

        # Initialize Font and Fontsize
        font = pygame.font.Font("freesansbold.ttf", 20)

        # Initialize Timer
        timer = pygame.time.Clock()

        # General Settings
        direction_command = 0
        startup_counter = 0
        counter = 0
        fps = 60

        # Power Up Settings
        power_up_time = 10.5
        power_up = False
        power_counter = 0
        flicker = False

        # PLAYER SETTINGS
        player_x = (WIDTH // 2) + x_offset
        player_y = 663 + y_offset
        player_size = (45, 45)
        player_direction = 0
        player_speed = 2
        lives = 3
        score = 0
        dot_nr = 0
        player_moving = False
        game_over = False
        game_won = False

        # GHOST SETTINGS
        ghost_size = (44, 44)
        ghost_speed_slow = 1
        ghost_speed_normal = 2
        ghost_speed_fast = 4
        ghost_speeds = [ghost_speed_normal,
                        ghost_speed_normal,
                        ghost_speed_normal,
                        ghost_speed_normal]
        eaten_ghosts = [False, False, False, False]
        targets = [(player_x, player_y), (player_x, player_y),
                (player_x, player_y), (player_x, player_y)]

        # BLINKY SETTINGS
        blinky_x = 56 + x_offset
        blinky_y = 58 + y_offset
        blinky_direction = 0
        blinky_dead = False
        blinky_box = False

        # INKY SETTINGS
        inky_x = (WIDTH //2) + x_offset
        inky_y = 388 + y_offset
        inky_direction = 2
        inky_dead = False
        inky_box = False

        # PINKY SETTINGS
        pinky_x = 380 + x_offset
        pinky_y = 438 + y_offset
        pinky_direction = 0
        pinky_dead = False
        pinky_box = False

        # CLYDE SETTINGS
        clyde_x = (WIDTH //2) + x_offset
        clyde_y = 438 + y_offset
        clyde_direction = 1
        clyde_dead = False
        clyde_box = False

        # Empty list of player images
        player_images = []

        # Resize player images and add to list
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(
                f'{PLAYER_IMG_PATH}{i}.png'), player_size))

        # Add ghost images
        blinky_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'red.png'), ghost_size)
        inky_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'blue.png'), ghost_size)
        pinky_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'pink.png'), ghost_size)
        clyde_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'orange.png'), ghost_size)
        spooked_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'powerup.png'), ghost_size)
        dead_img = pygame.transform.scale(pygame.image.load(
            GHOST_IMG_PATH + 'dead.png'), ghost_size)

        # - S O U N D S   A N D   M U S I C - #

        self.playing = False
        
        # Set booleans to play sounds once in loop
        enable_game_start_snd = True
        enable_eat_ghost_snd = True
        enable_death_1_snd = True

        # Define Pac Man Sound Files
        credit_snd = mixer.Sound(SOUNDS_PATH + "credit.mp3")
        death_1_snd = mixer.Sound(SOUNDS_PATH + "death_1.mp3")
        death_2_snd = mixer.Sound(SOUNDS_PATH + "death_2.mp3")
        eat_fruit_snd = mixer.Sound(SOUNDS_PATH + "eat_fruit.mp3")
        eat_ghost_snd = mixer.Sound(SOUNDS_PATH + "eat_ghost.mp3")
        extend_snd = mixer.Sound(SOUNDS_PATH + "extend.mp3")
        game_start_snd = mixer.Sound(SOUNDS_PATH + "game_start.mp3")
        intermission_snd = mixer.Sound(SOUNDS_PATH + "intermission.mp3")
        munch_1_snd = mixer.Sound(SOUNDS_PATH + "munch_1.mp3")
        munch_2_snd = mixer.Sound(SOUNDS_PATH + "munch_2.mp3")
        power_pellet_snd = mixer.Sound(SOUNDS_PATH + "power_pellet.mp3")
        retreating_snd = mixer.Sound(SOUNDS_PATH + "retreating.mp3")
        siren_1_snd = mixer.Sound(SOUNDS_PATH + "siren_1.mp3")
        siren_2_snd = mixer.Sound(SOUNDS_PATH + "siren_2.mp3")
        siren_3_snd = mixer.Sound(SOUNDS_PATH + "siren_3.mp3")
        siren_4_snd = mixer.Sound(SOUNDS_PATH + "siren_4.mp3")
        siren_5_snd = mixer.Sound(SOUNDS_PATH + "siren_5.mp3")

        # Define Sound Volumes
        mixer.music.set_volume(0.2)
        eat_ghost_snd.set_volume(0.5)

        # Ghost Class with behaviour of ghosts
        class Ghost:
            # All things the ghosts have in common
            def __init__(self, x_coord, y_coord, target, speed,
                        img, direction, dead, box, id, ghost_size):
                self.x_pos = x_coord
                self.y_pos = y_coord
                self.center_x = (self.x_pos - x_offset) + (ghost_size[0] // 2)
                self.center_y = (self.y_pos - y_offset) + (ghost_size[1] // 2)
                self.target = target
                self.speed = speed
                self.img = img
                self.direction = direction
                self.dead = dead
                self.in_box = box
                self.id = id
                self.turns, self.in_box = self.check_collisions()
                # Set Hitbox of ghosts
                self.rect = self.draw()

            def draw(self):
                # Power_up = Spooked Ghost | Dead = eyes ghost
                # Show regular ghost when no power up and not dead OR
                # When returned from box after being eaten and not dead at this time.
                if ((not power_up and not self.dead)
                        or (eaten_ghosts[self.id] and power_up and not self.dead)):
                    screen.blit(self.img, (self.x_pos, self.y_pos))
                # Show spooked ghost when Power Up active AND not dead AND not eaten
                elif power_up and not self.dead and not eaten_ghosts[self.id]:
                    screen.blit(spooked_img, (self.x_pos, self.y_pos))
                # Show dead ghost when above rules don't apply
                else:
                    screen.blit(dead_img, (self.x_pos, self.y_pos))
                # Return Ghost Rect (Hitbox)(set smaller for smaller hitbox)
                ghost_rect = (pygame.rect.Rect(
                    (self.center_x - 18, self.center_y - 18), (36, 36)))
                return ghost_rect

            def check_collisions(self):
                tile_height = ((HEIGHT - 50) // 32)  # num1
                tile_width = (WIDTH // 30)  # num2
                ghost_offset = 15
                # Turns (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                self.turns = [False, False, False, False]
                # Check if ghost is on board
                if 0 < self.center_x // 30 < 29:
                    # If above tile is Ghost Door then go up
                    if level[(self.center_y - ghost_offset) //
                            tile_height][self.center_x // tile_width] == 9:
                        self.turns[2] = True
                    # Check middle of player distance to allow LEFT
                    # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                    # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                    if level[self.center_y // tile_height][(
                        self.center_x - ghost_offset) // tile_width] < 3 \
                            or (level[self.center_y // tile_height][(
                                self.center_x - ghost_offset) // tile_width] == 9 and (
                                self.in_box or self.dead)):
                        self.turns[1] = True

                    # Check middle of player distance to allow RIGHT
                    # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                    # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                    if level[self.center_y // tile_height][(
                        self.center_x + ghost_offset) // tile_width] < 3 \
                            or (level[self.center_y // tile_height][(
                                self.center_x + ghost_offset) // tile_width] == 9 and (
                                self.in_box or self.dead)):
                        self.turns[0] = True

                    # Check middle of player distance to allow DOWN
                    # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                    # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                    if level[(self.center_y + ghost_offset) // tile_height][(
                        self.center_x // tile_width)] < 3 \
                            or (level[(self.center_y + ghost_offset) // tile_height][(
                                self.center_x // tile_width)] == 9 and (
                                self.in_box or self.dead)):
                        self.turns[3] = True

                    # Check middle of player distance to allow UP
                    # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                    # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                    if level[(self.center_y - ghost_offset) // tile_height][(
                        self.center_x // tile_width)] < 3 \
                            or (level[(self.center_y - ghost_offset) // tile_height][(
                            self.center_x // tile_width)] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True

                    # Direction (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    # When Moving UP or DOWN
                    if self.direction == 2 or self.direction == 3:
                        # Check middle of player distance to allow DOWN
                        # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                        # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                        if 12 <= self.center_x % tile_width <= 18:
                            if level[(self.center_y + ghost_offset) // tile_height][(
                                self.center_x // tile_width)] < 3 \
                                    or (level[(self.center_y + ghost_offset) //
                                            tile_height][self.center_x //
                                                        tile_width] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[3] = True

                            # Check middle of player distance to allow UP
                            # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                            # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                            if level[(self.center_y - ghost_offset) // tile_height][(
                                self.center_x // tile_width)] < 3 \
                                    or (level[(self.center_y - ghost_offset) //
                                            tile_height][self.center_x //
                                                        tile_width] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[2] = True

                        # Check middle of player distance to allow LEFT
                        # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                        # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                        if 12 <= self.center_y % tile_height <= 18:
                            if level[self.center_y // tile_height][(
                                self.center_x - tile_width) // tile_width] < 3 \
                                    or (level[self.center_y // tile_height][(
                                    self.center_x - tile_width) //
                                    tile_width] == 9 and (self.in_box or self.dead)):
                                self.turns[1] = True

                            # Check middle of player distance to allow RIGHT
                            # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                            # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                            if level[self.center_y // tile_height][(
                                self.center_x + tile_width) // tile_width] < 3 \
                                    or (level[self.center_y // tile_height][(
                                    self.center_x + tile_width) //
                                    tile_width] == 9 and (self.in_box or self.dead)):
                                self.turns[0] = True

                    # Direction (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    # When Moving LEFT or RIGHT
                    if self.direction == 0 or self.direction == 1:
                        # Check middle of player distance to allow DOWN
                        # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                        # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                        if 12<= self.center_x % tile_width <= 18:
                            if level[(self.center_y + ghost_offset) // tile_height][(
                                self.center_x // tile_width)] < 3 \
                                    or (level[(self.center_y + ghost_offset) //
                                            tile_height][self.center_x //
                                                        tile_width] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[3] = True

                            # Check middle of player distance to allow UP
                            # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                            # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                            if level[(self.center_y - ghost_offset) //
                                    tile_height][self.center_x // tile_width] < 3 \
                                    or (level[(self.center_y - ghost_offset) //
                                            tile_height][self.center_x //
                                                        tile_width] == 9 and (
                                    self.in_box or self.dead)):
                                self.turns[2] = True

                        # Check middle of player distance to allow LEFT
                        # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                        # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                        if 12 <= self.center_y % tile_height <= 18:
                            if level[self.center_y // tile_height][(
                                self.center_x - ghost_offset) // tile_width] < 3 \
                                    or (level[self.center_y // tile_height][(
                                    self.center_x - ghost_offset) //
                                    tile_width] == 9 and (self.in_box or self.dead)):
                                self.turns[1] = True

                            # Check middle of player distance to allow RIGHT
                            # level[row][column] < 3 (0=Empty 1=Small dot, 2=Big dot)
                            # OR 9 (9. Ghost Door) and Ghost in Box or Dead
                            if level[self.center_y // tile_height][(
                                self.center_x + ghost_offset) // tile_width] < 3 \
                                    or (level[self.center_y // tile_height][(
                                    self.center_x + ghost_offset) //
                                    tile_width] == 9 and (self.in_box or self.dead)):
                                self.turns[0] = True
                else:
                    self.turns[0] = True
                    self.turns[1] = True

                # Are ghosts in box?
                if 350 + x_offset < self.x_pos < 550 + x_offset and 370 + y_offset < self.y_pos < 480 + y_offset:
                    self.in_box = True
                else:
                    self.inbox = False
                return self.turns, self.in_box

            def move_clyde(self):
                # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                # Clyde is going to turn whenever advantageous for pursuit

                # When moving RIGHT
                if self.direction == 0:
                    # Target X pos higher then own X pos (target = RIGHT)
                    # AND able to still go RIGHT. Then keep going RIGHT
                    if self.target[0] > self.x_pos and self.turns[0]:
                        # Keep moving RIGHT
                        self.x_pos += self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to RIGHT and not able to go UP or DOWN
                        # Then just go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Target Y pos higher then own Y pos (target = UP)
                        # AND able to turn DOWN. Then go UP
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # If UP or DOWN is no option then just go RIGHT
                        # When moving RIGHT, going LEFT is strange
                        else:
                            self.x_pos += self.speed

                # When moving LEFT
                elif self.direction == 1:
                    # When moving LEFT and option to go DOWN then DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        # self.y_pos += self.speed

                    # Target X pos smaller then own X pos (target = LEFT)
                    # AND able to still go LEFT. Then keep going LEFT
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        # Keep moving LEFT
                        self.x_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Target Y pos higher then own Y pos (target = UP)
                        # AND able to turn DOWN. Then go UP
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # If UP or DOWN is no option then just go LEFT
                        # When moving LEFT, going RIGHT is strange
                        else:
                            self.x_pos -= self.speed

                # When moving UP
                elif self.direction == 2:
                    # When moving UP and option to go LEFT then LEFT
                    if self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed

                    # Target Y pos smaller then own Y pos (target = UP)
                    # AND able to still go UP. Then keep going UP
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        # Keep moving UP
                        self.y_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go UP if possible
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # Target X pos higher then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # If LEFT or RIGHT is no option then just go UP
                        # When moving UP, going DOWN is strange
                        else:
                            self.y_pos -= self.speed

                # When moving DOWN
                elif self.direction == 3:
                    # When moving DOWN keep going DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    # When not able to keep going DOWN make decision
                    elif not self.turns[3]:
                        # When moving DOWN and option to go RIGHT then RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # When moving DOWN and option to go LEFT then LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # When moving DOWN and target is UP go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed

                        # Go UP
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[3]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # Target X pos higher then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # If LEFT or RIGHT is no option then just go DOWN
                        # When moving DOWN, going UP is strange
                        else:
                            self.y_pos += self.speed

                if self.x_pos < -30 + x_offset:
                    self.x_pos = 900 + x_offset
                elif self.x_pos > 900 + x_offset:
                    self.x_pos = - 30 + x_offset
                return self.x_pos, self.y_pos, self.direction

            def move_blinky(self):
                # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                # Clyde is going to turn whenever colliding with walls,
                # otherwise continue straight

                # When moving RIGHT
                if self.direction == 0:
                    # Target X pos higher then own X pos (target = RIGHT)
                    # AND able to still go RIGHT. Then keep going RIGHT
                    if self.target[0] > self.x_pos and self.turns[0]:
                        # Keep moving RIGHT
                        self.x_pos += self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to RIGHT and not able to go UP or DOWN
                        # Then just go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[0]:
                        # Keep going RIGHT
                        self.x_pos += self.speed

                # When moving LEFT
                elif self.direction == 1:
                    # Target X pos smaller then own X pos (target = LEFT)
                    # AND able to still go LEFT. Then keep going LEFT
                    if self.target[0] < self.x_pos and self.turns[1]:
                        # Keep moving LEFT
                        self.x_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[1]:
                        # Keep Going LEFT
                        self.x_pos -= self.speed

                # When moving UP
                elif self.direction == 2:
                    # Target Y pos smaller then own Y pos (target = UP)
                    # AND able to still go UP. Then keep going UP
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        # Keep moving UP
                        self.y_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed

                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed

                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go UP if possible
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[2]:
                        # Keep going UP
                        self.y_pos -= self.speed

                # When moving DOWN
                elif self.direction == 3:
                    # When moving DOWN keep going DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    # When not able to keep going DOWN make decision
                    elif not self.turns[3]:
                        # When moving DOWN and option to go RIGHT then RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # When moving DOWN and option to go LEFT then LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # When moving DOWN and target is UP go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed

                        # Go UP
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed

                        # Go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                        # Go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[3]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # Target X pos higher then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # If LEFT or RIGHT is no option then just go DOWN
                        # When moving DOWN, going UP is strange
                        else:
                            self.y_pos += self.speed

                if self.x_pos < -30 + x_offset:
                    self.x_pos = 900 + x_offset
                elif self.x_pos > 900 + x_offset:
                    self.x_pos = - 30 + x_offset
                return self.x_pos, self.y_pos, self.direction

            def move_inky(self):
                # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                # Inky turns up or down at any point to pursue,
                # but left and right only on collision

                # When moving RIGHT
                if self.direction == 0:
                    # Target X pos higher then own X pos (target = RIGHT)
                    # AND able to still go RIGHT. Then keep going RIGHT
                    if self.target[0] > self.x_pos and self.turns[0]:
                        # Keep moving RIGHT
                        self.x_pos += self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to RIGHT and not able to go UP or DOWN
                        # Then just go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Target Y pos higher then own Y pos (target = UP)
                        # AND able to turn DOWN. Then go UP
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # If UP or DOWN is no option then just go RIGHT
                        # When moving RIGHT, going LEFT is strange
                        else:
                            self.x_pos += self.speed

                # When moving LEFT
                elif self.direction == 1:
                    # When moving LEFT and option to go DOWN then DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        # self.y_pos += self.speed

                    # Target X pos smaller then own X pos (target = LEFT)
                    # AND able to still go LEFT. Then keep going LEFT
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        # Keep moving LEFT
                        self.x_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Target Y pos higher then own Y pos (target = UP)
                        # AND able to turn DOWN. Then go UP
                        if self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # If UP or DOWN is no option then just go LEFT
                        # When moving LEFT, going RIGHT is strange
                        else:
                            self.x_pos -= self.speed

                # When moving UP
                elif self.direction == 2:
                    # Target Y pos smaller then own Y pos (target = UP)
                    # AND able to still go UP. Then keep going UP
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        # Keep moving UP
                        self.y_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go UP if possible
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[2]:
                        self.y_pos -= self.speed

                # When moving DOWN
                elif self.direction == 3:
                    # When moving DOWN keep going DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    # When not able to keep going DOWN make decision
                    elif not self.turns[3]:
                        # When moving DOWN and option to go RIGHT then RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # When moving DOWN and option to go LEFT then LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # When moving DOWN and target is UP go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed

                        # Go UP
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[3]:
                        self.y_pos += self.speed

                if self.x_pos < -30 + x_offset:
                    self.x_pos = 900 + x_offset
                elif self.x_pos > 900 + x_offset:
                    self.x_pos = - 30 + x_offset
                return self.x_pos, self.y_pos, self.direction

            def move_pinky(self):
                # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                # Pinky is going to turn left or right whenever advantageous,
                # but only up or down on collision

                # When moving RIGHT
                if self.direction == 0:
                    # Target X pos higher then own X pos (target = RIGHT)
                    # AND able to still go RIGHT. Then keep going RIGHT
                    if self.target[0] > self.x_pos and self.turns[0]:
                        # Keep moving RIGHT
                        self.x_pos += self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[0]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to RIGHT and not able to go UP or DOWN
                        # Then just go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[0]:
                        self.x_pos += self.speed

                # When moving LEFT
                elif self.direction == 1:
                    # When moving LEFT and option to go DOWN then DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        # self.y_pos += self.speed

                    # Target X pos smaller then own X pos (target = LEFT)
                    # AND able to still go LEFT. Then keep going LEFT
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        # Keep moving LEFT
                        self.x_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[1]:
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        if self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed
                        # Target Y pos smaller then own Y pos (target = UP)
                        # AND able to turn UP. Then go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            # Turn direction to UP
                            self.direction = 2
                            # Start moving UP
                            self.y_pos -= self.speed
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        elif self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Go UP if possible
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[1]:
                        self.x_pos -= self.speed

                # When moving UP
                elif self.direction == 2:
                    # When moving UP and option to go LEFT then LEFT
                    if self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed

                    # Target Y pos smaller then own Y pos (target = UP)
                    # AND able to still go UP. Then keep going UP
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        # Keep moving UP
                        self.y_pos -= self.speed

                    # If there is a collision make a decision to turn
                    elif not self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            # Turn direction to RIGHT
                            self.direction = 0
                            # Start moving RIGHT
                            self.x_pos += self.speed
                        # Target X pos smaller then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            # Turn direction to LEFT
                            self.direction = 1
                            # Start moving LEFT
                            self.x_pos -= self.speed
                        # Target Y pos higher then own Y pos (target = DOWN)
                        # AND able to turn DOWN. Then go DOWN
                        elif self.target[1] > self.y_pos and self.turns[3]:
                            # Turn direction to DOWN
                            self.direction = 3
                            # Start moving DOWN
                            self.y_pos += self.speed

                        # WHEN ABOVE NOT APPLY MAKE ANOTHER CHOICE
                        # Go UP if possible
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go DOWN if possible
                        elif self.turns[3]:
                            self.direction = 3
                            self.y_pos += self.speed
                        # Moving to LEFT and not able to go UP or DOWN
                        # Then just go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[2]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # Target X pos higher then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # If LEFT or RIGHT is no option then just go UP
                        # When moving UP, going DOWN is strange
                        else:
                            self.y_pos -= self.speed

                # When moving DOWN
                elif self.direction == 3:
                    # When moving DOWN keep going DOWN
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.y_pos += self.speed
                    # When not able to keep going DOWN make decision
                    elif not self.turns[3]:
                        # When moving DOWN and option to go RIGHT then RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # When moving DOWN and option to go LEFT then LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # When moving DOWN and target is UP go UP
                        elif self.target[1] < self.y_pos and self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed

                        # Go UP
                        elif self.turns[2]:
                            self.direction = 2
                            self.y_pos -= self.speed
                        # Go LEFT
                        elif self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # Go RIGHT
                        elif self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed

                    # If there is NO collision make a decision to turn
                    # Move (0=RIGHT, 1=LEFT, 2=UP, 3=DOWN)
                    elif self.turns[3]:
                        # Target X pos higher then own X pos (target = RIGHT)
                        # AND able to turn RIGHT. Then go RIGHT
                        if self.target[0] > self.x_pos and self.turns[0]:
                            self.direction = 0
                            self.x_pos += self.speed
                        # Target X pos higher then own X pos (target = LEFT)
                        # AND able to turn LEFT. Then go LEFT
                        elif self.target[0] < self.x_pos and self.turns[1]:
                            self.direction = 1
                            self.x_pos -= self.speed
                        # If LEFT or RIGHT is no option then just go DOWN
                        # When moving DOWN, going UP is strange
                        else:
                            self.y_pos += self.speed

                if self.x_pos < -30 + x_offset:
                    self.x_pos = 900 + x_offset
                elif self.x_pos > 900 + x_offset:
                    self.x_pos = - 30 + x_offset
                return self.x_pos, self.y_pos, self.direction


        # Reset Pac-Man and Ghosts
        # (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
        def reset(player_x, player_y, player_direction, direction_command,
                startup_counter, power_up, power_counter,
                blinky_x, blinky_y, blinky_direction, blinky_dead,
                inky_x, inky_y, inky_direction, inky_dead,
                pinky_x, pinky_y, pinky_direction, pinky_dead,
                clyde_x, clyde_y, clyde_direction, clyde_dead,
                eaten_ghosts):

            # Reset Player settings
            player_x = (WIDTH // 2) + x_offset
            player_y = 663 + y_offset
            player_direction = 0
            direction_command = 0
            startup_counter = 0
            power_counter = 0
            power_up = False

            # Reset Blinky settings
            blinky_x = 56 + x_offset
            blinky_y = 58 + y_offset
            blinky_direction = 0
            blinky_dead = False

            # RESET INKY SETTINGS
            inky_x = (WIDTH //2) + x_offset
            inky_y = 388 + y_offset
            inky_direction = 2
            inky_dead = False

            # RESET PINKY SETTINGS
            pinky_x = 380 + x_offset
            pinky_y = 438 + y_offset
            pinky_direction = 0
            pinky_dead = False

            # RESET CLYDE SETTINGS
            clyde_x = (WIDTH //2) + x_offset
            clyde_y = 438 + y_offset
            clyde_direction = 1
            clyde_dead = False

            # Reset Eaten Ghosts
            eaten_ghosts = [False, False, False, False]

            return(player_x, player_y, player_direction,
                direction_command, startup_counter, power_up, power_counter,
                blinky_x, blinky_y, blinky_direction, blinky_dead,
                inky_x, inky_y, inky_direction, inky_dead,
                pinky_x, pinky_y, pinky_direction, pinky_dead,
                clyde_x, clyde_y, clyde_direction, clyde_dead, eaten_ghosts)

        # Draw other stuff on the board
        def draw_misc():
            # Render font. (Put in a True for smoother edges on font)
            score_text = font.render(f'Score: {score}', True, text_color)
            screen.blit(score_text, (10 + x_offset, 920 + y_offset))
            # if power_up:
            #     pygame.draw.circle(screen, "blue", (140, 930), 15)
            for i in range(lives):
                screen.blit(pygame.transform.scale(
                    player_images[0], (30, 30)), (650 + i * 40 + x_offset, 915 + y_offset))
            if game_over:
                pygame.draw.rect(screen, 'white', [50 + x_offset, 200 + y_offset, 800, 300], 0, 10)
                pygame.draw.rect(screen, 'dark gray', [70 + x_offset, 220 + y_offset, 760, 260], 0, 10)
                game_over_text = font.render(
                    "Game over! Space bar to restart!", True, "red")
                screen.blit(game_over_text, (100 + x_offset, 300 + y_offset))
            if game_won:
                pygame.draw.rect(screen, 'white', [50 + x_offset, 200 + y_offset, 800, 300], 0, 10)
                pygame.draw.rect(screen, 'dark gray', [70 + x_offset, 220 + y_offset, 760, 260], 0, 10)
                game_over_text = font.render(
                    "Victory! Space bar to restart!", True, "green")
                screen.blit(game_over_text, (100 + x_offset, 300 + y_offset))

        # Check if Pacman colide with something
        def check_collisions(score, power_up, power_counter, eaten_ghosts, dot_nr):
            tile_height = ((HEIGHT - 50) // 32)  # num1
            tile_width = (WIDTH // 30)  # num2
            # If player is on the board
            if 0 + x_offset < player_x < (WIDTH - tile_width) + x_offset:
                # Is there a small dot to eat at player location?
                # [ROW][COLUMN] = 1 (dot)
                if level[center_y // tile_height][center_x // tile_width] == 1:
                    dot_nr += 1
                    # Play munch_1_snd and munch_2_snd
                    # Start at second dot, first one gets eaten at start
                    if dot_nr > 1:
                        munch_1_snd.play()
                        munch_2_snd.play()
                    # Then remove small dot (0 = empty tile)
                    level[center_y // tile_height][center_x // tile_width] = 0
                    # Update score
                    score += 10

                # Is there a big dot to eat at player location?
                # [ROW][COLUMN] = 2 (big dot)
                if level[center_y // tile_height][center_x // tile_width] == 2:
                    # Then remove big dot (0 = empty tile)
                    level[center_y // tile_height][center_x // tile_width] = 0
                    # Update score
                    score += 50
                    # Play power_pellet sound
                    power_pellet_snd.play(loops=4)
                    # Power on
                    power_up = True
                    # Reset power for when another power was already active
                    power_counter = 0
                    # List of eaten ghosts
                    eaten_ghosts = [False, False, False, False]
            return score, power_up, power_counter, eaten_ghosts, dot_nr

        # Draw Board for this level
        def draw_board():
            # Tile Size Pacman board has 32 x 30 Tiles
            # (height - 50 because of padding at bottom for extra info)
            # // = Floor division and gives back Integers which we need
            tile_height = ((HEIGHT - 50) // 32)  # num1
            tile_width = (WIDTH // 30)  # num2
            # iterate thru every single row of the board
            for row in range(len(level)):  # i
                # iterate thru every single column of a row
                for column in range(len(level[row])):  # j
                    # 1. Small dot
                    if level[row][column] == 1:
                        # draw a circle on screen, white color,
                        # (x coordinate in center), (y coordinate in center), size of radius
                        pygame.draw.circle(screen, small_dot_color,
                                        (column * tile_width + (0.5 * tile_width) + x_offset, row * tile_height + (0.5 * tile_height) + y_offset), 4)

                    # 2. Big dot (power up)
                    if level[row][column] == 2 and not flicker:
                        # draw a circle on screen, white color,
                        # (x coordinate in center),
                        # (y coordinate in center), size of radius
                        pygame.draw.circle(screen, big_dot_color,
                                        (column * tile_width + (0.5 * tile_width) + x_offset, row * tile_height + (0.5 * tile_height) + y_offset), 10)

                    # 3. Vertical Lines
                    if level[row][column] == 3:
                        # draw a line on screen, blue color,
                        # (x coordinate in center),
                        # (y coordinate in center), line thickness
                        pygame.draw.line(screen, line_color,
                                        # Start position of line (centered)
                                        (column * tile_width + (0.5 * tile_width) + x_offset, row * tile_height + y_offset),
                                        # End position of line (centered)
                                        (column * tile_width + (0.5 * tile_width)+ x_offset, row * tile_height + tile_height + y_offset), 3)

                    # 4. Horizontal Lines
                    if level[row][column] == 4:
                        # draw a line on screen, blue color,
                        # (x coordinate in center),
                        # (y coordinate in center), line thickness
                        pygame.draw.line(screen, line_color,
                                        # Start position of line (centered)
                                        (column * tile_width + x_offset, row * tile_height + (0.5 * tile_height) + y_offset),
                                        # End position of line (centered)
                                        (column * tile_width + tile_width + x_offset, row * tile_height + (0.5 * tile_height) + y_offset), 3)

                    # 5. Right Top Corner Curve
                    if level[row][column] == 5:
                        # Draw a rectangle in a rectangle and give it a curve
                        pygame.draw.arc(screen, line_color,
                                        # Little tweaked for better aligning
                                        [(column * tile_width - (0.4 * tile_width) - 2 + x_offset),
                                        (row * tile_height + (0.5 * tile_height) + 1 + y_offset), tile_width, tile_height], 0, PI/2, 3)

                    # 6. Left Top Corner Curve
                    if level[row][column] == 6:
                        # Draw a rectangle in a rectangle and give it a curve
                        pygame.draw.arc(screen, line_color,
                                        # Little tweaked for better aligning
                                        [(column * tile_width + (0.5 * tile_width) + 1 + x_offset),
                                        (row * tile_height + (0.5 * tile_height) + 1 + y_offset), tile_width, tile_height], PI/2, PI,3)

                    # 7. Left Bottom Corner Curve
                    if level[row][column] == 7:
                        # Draw a rectangle in a rectangle and give it a curve
                        pygame.draw.arc(screen, line_color,
                                        # Little tweaked for better aligning
                                        [(column * tile_width + (0.4 * tile_width) + 4 + x_offset),
                                        (row * tile_height - (0.4 * tile_height) - 2 + y_offset), tile_width, tile_height], PI, 3 * PI/2, 3)

                    # 8. Right Bottom Corner Curve
                    if level[row][column] == 8:
                        # Draw a rectangle in a rectangle and give it a curve
                        pygame.draw.arc(screen, line_color,
                                        # Little tweaked for better aligning
                                        [(column * tile_width - (0.4 * tile_width)- 2 + x_offset),
                                        (row * tile_height - (0.4 * tile_height) - 2 + y_offset), tile_width, tile_height], 3 * PI/2, 2 * PI,3)

                    # 9. Ghost Door
                    if level[row][column] == 9:
                        # draw a line on screen, blue color,
                        # (x coordinate in center),
                        # (y coordinate in center), line thickness
                        pygame.draw.line(screen, door_color,
                                        # Start position of line (centered)
                                        (column * tile_width + x_offset, row * tile_height + (0.5 * tile_height)+ y_offset),
                                        # End position of line (centered)
                                        (column * tile_width + tile_width + x_offset, row * tile_height + (0.5 * tile_height)+ y_offset), 3)

        # Draw Player
        def draw_player():
            # 0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN
            if player_direction == 0:
                screen.blit(player_images[counter // 5], (player_x, player_y))
            elif player_direction == 1:
                screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
            elif player_direction == 2:
                screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
            elif player_direction == 3:
                screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

        # Check Player Position and return possible movements
        def check_position(center_x, center_y):
            # Turns (RIGHT, LEFT, UP, DOWN)
            turns = [False, False, False, False]
            tile_height = ((HEIGHT - 50) // 32)  # num1
            tile_width = (WIDTH // 30)  # num2
            player_offset = 15

            # Check collisions based on center_x and center_y of
            # player +/- player_offset

            # First check if player is on the board
            if center_x // 30 < 29:

                # Facing RIGHT
                if player_direction == 0:

                    # level[row][column] < 3 (1. Small dot, 2. Big dot (power up))
                    if level[center_y // tile_height][(center_x - player_offset) // tile_width] < 3:

                        # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                        turns[1] = True

                # Facing LEFT
                if player_direction == 1:

                    # level[row][column] < 3 (1. Small dot, 2. Big dot (power up))
                    if level[center_y // tile_height][(center_x + player_offset) // tile_width] < 3:

                        # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                        turns[0] = True

                # Facing UP
                if player_direction == 2:

                    # level[row][column] < 3 (1. Small dot, 2. Big dot (power up))
                    if level[(center_y + player_offset) // tile_height][center_x // tile_width] < 3:

                        # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                        turns[3] = True

                # Facing DOWN
                if player_direction == 3:

                    # level[row][column] < 3 (1. Small dot, 2. Big dot (power up))
                    if level[(center_y - player_offset) // tile_height][center_x // tile_width] < 3:

                        # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                        turns[2] = True

                # Moving UP or DOWN
                if player_direction == 2 or player_direction == 3:

                    # Check middle of player distance to allow up and down
                    if 12 <= center_x % tile_width <= 18:

                        # If tile below is open then enable player_direction DOWN
                        if level[(center_y + player_offset) // tile_height][center_x // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[3] = True

                        # If tile above is open then enable player_direction UP
                        if level[(center_y - player_offset) // tile_height][center_x // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[2] = True

                    # Check middle of player distance to allow left and right
                    if 12 <= center_y % tile_height <= 18:
                        
                        # If tile below is open then enable player_direction DOWN
                        if level[center_y // tile_height][(center_x - tile_width) // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[1] = True

                        # If tile above is open then enable player_direction UP
                        if level[center_y // tile_height][(center_x + tile_width) // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[0] = True

                # Moving LEFT or RIGHT
                if player_direction == 0 or player_direction == 1:

                    # Check middle of player distance to allow up and down
                    if 12 <= center_x % tile_width <= 18:

                        # If tile below is open then enable player_direction DOWN
                        if level[(center_y + tile_height) // tile_height][center_x // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[3] = True

                        # If tile above is open then enable player_direction UP
                        if level[(center_y - tile_height) // tile_height][center_x // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[2] = True

                    # Check middle of player distance to allow left and right
                    if 12 <= center_y % tile_height <= 18:

                        # If tile below is open then enable player_direction DOWN
                        if level[center_y // tile_height][(center_x - player_offset) // tile_width] < 3:

                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[1] = True

                        # If tile above is open then enable player_direction UP
                        if level[center_y // tile_height][(center_x + player_offset) // tile_width] < 3:
                            
                            # Turns (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                            turns[0] = True
            else:
                # If player goes outside board then only LEFT and RIGHT are possible
                turns[0] = True
                turns[1] = True
            return turns

        # Move Player (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
        def move_player(player_x, player_y):
            # If RIGHT player_direction is alowed
            if player_direction == 0 and turns_alowed[0]:
                # Increase X position with player speed
                player_x += player_speed
            # If LEFT player_direction is alowed
            elif player_direction == 1 and turns_alowed[1]:
                # Decrease X position with player speed
                player_x -= player_speed
            # If UP player_direction is alowed
            elif player_direction == 2 and turns_alowed[2]:
                # Decrease Y position with player speed
                player_y -= player_speed
            # If DOWN player_direction is alowed
            elif player_direction == 3 and turns_alowed[3]:
                # Increase Y position with player speed
                player_y += player_speed
            # Return new values for X and Y position
            return player_x, player_y

        # Targets
        def get_targets(blinky_x, blinky_y,
                        inky_x, inky_y,
                        pinky_x, pinky_y,
                        clyde_x, clyde_y):
            # If player is on left side of board while Power Up is Active
            if player_x < (WIDTH // 2) + x_offset:
                # Go to other side of board
                runaway_x = WIDTH + x_offset
            else:
                runaway_x = 0 + x_offset
            if player_y < (HEIGHT // 2) + y_offset:
                # Go to other side of board
                runaway_y = HEIGHT + y_offset
            else:
                runaway_y = 0 + y_offset

            # Target location of box when eaten
            return_target = (380 + x_offset, 400 + y_offset)

            # When Power Up is Active
            if power_up:
                # If Blinky is alive
                if not blinky.dead and not eaten_ghosts[0]:
                    blinky_target = (runaway_x, runaway_y)
                # Is Blinky in Box?
                elif not blinky.dead and eaten_ghosts[0]:
                    if 340 + x_offset < blinky_x < 560 + x_offset and 340 + y_offset < blinky_y < 500 + y_offset:
                        # Go out of box
                        blinky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase Player
                        blinky_target = (player_x , player_y)
                # If Blinky is dead
                else:
                    # Go to box
                    blinky_target = return_target

                # If Inky is alive
                if not inky.dead and not eaten_ghosts[1]:
                    inky_target = (runaway_x, player_y)
                # Is Inky in Box?
                elif not inky.dead and eaten_ghosts[1]:
                    if 340 + x_offset < inky_x < 560 + x_offset and 340 + y_offset < inky_y < 500 + y_offset:
                        # Go out of box
                        inky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase Player
                        inky_target = (player_x, player_y)
                # If Inky is dead
                else:
                    # Go to box
                    inky_target = return_target

                # If Pinky is alive
                if not pinky.dead:
                    pinky_target = (player_x, runaway_y)
                elif not pinky.dead and not eaten_ghosts[2]:
                    # Is Pinky in Box?
                    if 340 + x_offset< pinky_x < 560 + x_offset and 340 + y_offset < pinky_y < 500 + y_offset:
                        # Go out of box
                        pinky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase Player
                        pinky_target = (player_x, player_y)
                # If Pinky is dead
                else:
                    # Go to box
                    pinky_target = return_target

                # If Clyde is alive
                if not clyde.dead and not eaten_ghosts[3]:
                    clyde_target = (450 + x_offset, 450 + y_offset)
                # Is Clyde in Box?
                elif not clyde.dead and eaten_ghosts[3]:
                    if 340 + x_offset < clyde_x < 560 + x_offset and 340 + y_offset < clyde_y < 500 + y_offset:
                        # Go out of box
                        clyde_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase Player
                        clyde_target = (player_x, player_y)
                # If Clyde is dead
                else:
                    # Go to box
                    clyde_target = return_target

            # When Power Up is NOT Active
            else:
                # If Blinky is alive
                if not blinky.dead:
                    # Is Blinky in Box?
                    if 340 + x_offset < blinky_x < 560 + x_offset and 340 + y_offset < blinky_y < 500 + y_offset:
                        # Go out of box
                        blinky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase player
                        blinky_target = (player_x, player_y)
                # If Blinky is dead
                else:
                    # Go to box
                    blinky_target = return_target

                # If Inky is alive
                if not inky.dead:
                    # Is inky in Box?
                    if 340 + x_offset < inky_x < 560 + x_offset and 340 + y_offset < inky_y < 500 + y_offset:
                        # Go out of box
                        inky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase player
                        inky_target = (player_x, player_y)
                # If inky is dead
                else:
                    # Go to box
                    inky_target = return_target

                # If Pinky is alive
                if not pinky.dead:
                    # Is pinky in Box?
                    if 340 + x_offset < pinky_x < 560 + x_offset and 340 + y_offset < pinky_y < 500 + y_offset:
                        # Go out of box
                        pinky_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase player
                        pinky_target = (player_x, player_y)
                # If inky is dead
                else:
                    # Go to box
                    pinky_target = return_target

                # If Clyde is alive
                if not clyde.dead:
                    # Is clyde in Box?
                    if 340 + x_offset < clyde_x < 560 + x_offset and 340 + y_offset < clyde_y < 500 + y_offset:
                        # Go out of box
                        clyde_target = (425 + x_offset, 100 + y_offset)
                    else:
                        # Chase player
                        clyde_target = (player_x, player_y)
                # If Clyde is dead
                else:
                    # Go to box
                    clyde_target = return_target

            return [blinky_target, inky_target, pinky_target, clyde_target]

        # Game Loop
        run = True
        while run:
            # Set framerate
            timer.tick(fps)

            # Counter
            if counter < 19:
                counter += 1
                # Big dot flicker speed
                if counter > 9:
                    flicker = False
            else:
                counter = 0
                flicker = True

            # Power Up (lasts 10 sec. X FPS = 600)
            power_up_timer = power_up_time * fps
            if power_up and power_counter < power_up_timer:
                power_counter += 1
            elif power_up and power_counter >= power_up_timer:
                power_counter = 0
                power_up = False
                eaten_ghosts = [False, False, False, False]

            # Startup delay of 4 seconds
            if startup_counter < 240 and not game_over and not game_won:
                player_moving = False
                # Play Game Start sound
                if enable_game_start_snd:
                    game_start_snd.play(loops=0)
                    enable_game_start_snd = False
                # Enable death_1 Sound
                enable_death_1_snd = True
                startup_counter += 1
            else:
                player_moving = True

            # Set background color
            screen.fill(BG_COLOR)

            # Draw Board
            draw_board()

            # Define center of the player
            center_x = (player_x - x_offset) + (player_size[0] // 2)
            center_y = (player_y - y_offset) + (player_size[1] // 2)

            # Change ghost speed when powerup active
            if power_up:
                # Slow down when powerup active
                ghost_speeds = [ghost_speed_slow,
                                ghost_speed_slow,
                                ghost_speed_slow,
                                ghost_speed_slow]

            # Normal speed when no powerup active
            else:
                ghost_speeds = [ghost_speed_normal,
                                ghost_speed_normal,
                                ghost_speed_normal,
                                ghost_speed_normal]

            # Normal Speed when ghost is alive after dead
            if eaten_ghosts[0]:
                ghost_speeds[0] = ghost_speed_normal
            if eaten_ghosts[1]:
                ghost_speeds[1] = ghost_speed_normal
            if eaten_ghosts[2]:
                ghost_speeds[2] = ghost_speed_normal
            if eaten_ghosts[3]:
                ghost_speeds[3] = ghost_speed_normal

            # Speed up when ghost is dead
            if blinky_dead:
                ghost_speeds[0] = ghost_speed_fast
            if inky_dead:
                ghost_speeds[1] = ghost_speed_fast
            if pinky_dead:
                ghost_speeds[2] = ghost_speed_fast
            if clyde_dead:
                ghost_speeds[3] = ghost_speed_fast

            game_won = True
            # Check if there are dots on board
            for i in range(len(level)):
                if 1 in level[i] or 2 in level[i]:
                    game_won = False

            # Define Players Hitbox (invisible behind player image)
            player_hitbox = pygame.draw.circle(screen, background_color,
                (center_x, center_y), (player_size[0] // 2) - 2, 2)

            # Draw Player
            draw_player()

            # Draw Blinky Ghost
            blinky = Ghost(
                blinky_x, blinky_y,
                targets[0], ghost_speeds[0],
                blinky_img, blinky_direction,
                blinky_dead, blinky_box, 0, ghost_size)

            # Draw Inky Ghost
            inky = Ghost(
                inky_x, inky_y,
                targets[1], ghost_speeds[1],
                inky_img, inky_direction,
                inky_dead, inky_box, 1, ghost_size)

            # Draw Pinky Ghost
            pinky = Ghost(
                pinky_x, pinky_y,
                targets[2], ghost_speeds[2],
                pinky_img, pinky_direction,
                pinky_dead, pinky_box, 2, ghost_size)

            # Draw Clyde Ghost
            clyde = Ghost(
                clyde_x, clyde_y,
                targets[3], ghost_speeds[3],
                clyde_img, clyde_direction,
                clyde_dead, clyde_box, 3, ghost_size)

            # Draw Misc
            draw_misc()

            # Targets
            targets = get_targets(blinky_x, blinky_y,
                                inky_x, inky_y,
                                pinky_x, pinky_y,
                                clyde_x, clyde_y)

            # Check position of player
            turns_alowed = check_position(center_x, center_y)

            # Update player and ghosts X and Y values when player_moving
            if player_moving:
                player_x, player_y = move_player(player_x, player_y)
                # Move like Blinky when alive and not in box 
                if not blinky_dead and not blinky.in_box:
                    blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                else:
                    blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                if not inky_dead and not inky.in_box:
                    inky_x, inky_y, inky_direction = inky.move_inky()
                else:
                    inky_x, inky_y, inky_direction = inky.move_clyde()
                if not pinky_dead and not pinky.in_box:
                    pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                else:
                    pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

            # Check if Pac-Man colide with something
            score, power_up, power_counter, eaten_ghosts, dot_nr = check_collisions(
                score, power_up, power_counter, eaten_ghosts, dot_nr)

            # Check if Pac-Man colide with ghosts
            # Power Up is NOT Active
            if not power_up:
                # If player colide with Ghost and Ghost is not dead
                if (player_hitbox.colliderect(blinky.rect) and not blinky.dead
                        or player_hitbox.colliderect(inky.rect) and not inky.dead
                        or player_hitbox.colliderect(pinky.rect) and not pinky.dead
                        or player_hitbox.colliderect(clyde.rect) and not clyde.dead):
                    # Play death_1 sound once
                    if enable_death_1_snd:
                        death_1_snd.play(loops=0)
                        enable_death_1_snd = False
                    # Check if player has lives left
                    if lives > 0:
                        # Subtract one live
                        lives -= 1

                        # Reset Pac-Man and Ghosts
                        (player_x, player_y, player_direction,
                            direction_command, startup_counter, power_up,
                            power_counter,
                            blinky_x, blinky_y, blinky_direction, blinky_dead,
                            inky_x, inky_y, inky_direction, inky_dead,
                            pinky_x, pinky_y, pinky_direction, pinky_dead,
                            clyde_x, clyde_y, clyde_direction, clyde_dead,
                            eaten_ghosts) = reset(
                            player_x, player_y, player_direction,
                            direction_command, startup_counter, power_up,
                            power_counter,
                            blinky_x, blinky_y, blinky_direction, blinky_dead,
                            inky_x, inky_y, inky_direction, inky_dead,
                            pinky_x, pinky_y, pinky_direction, pinky_dead,
                            clyde_x, clyde_y, clyde_direction, clyde_dead,
                            eaten_ghosts)
                    else:
                        game_over = True
                        player_moving = False
                        startup_counter = 0
                        # Play death_1 sound once
                        if enable_death_1_snd:
                            death_1_snd.play(loops=0)
                            enable_death_1_snd = False

            # Power Up is Active, colide with Blinky while already eaten
            if (power_up and player_hitbox.colliderect(blinky.rect)
                    and eaten_ghosts[0] and not blinky.dead):
                # Check if player has lives left
                if lives > 0:
                    # Subtract one live
                    lives -= 1

                    # Reset Pac-Man and Ghosts
                    (player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts) = reset(
                        player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts)
                else:
                    game_over = True
                    player_moving = False
                    startup_counter = 0

            # Power Up is Active, colide with Inky while already eaten
            if (power_up and player_hitbox.colliderect(inky.rect)
                    and eaten_ghosts[1] and not inky.dead):
                # Check if player has lives left
                if lives > 0:
                    # Subtract one live
                    lives -= 1

                    # Reset Pac-Man and Ghosts
                    (player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts) = reset(
                        player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts)
                else:
                    game_over = True
                    player_moving = False
                    startup_counter = 0

            # Power Up is Active, colide with Pinky while already eaten
            if (power_up and player_hitbox.colliderect(pinky.rect)
                    and eaten_ghosts[2] and not pinky.dead):
                # Check if player has lives left
                if lives > 0:
                    # Subtract one live
                    lives -= 1

                    # Reset Pac-Man and Ghosts
                    (player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts) = reset(
                        player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts)
                else:
                    game_over = True
                    player_moving = False
                    startup_counter = 0

            # Power Up is Active, colide with Clyde while already eaten
            if (power_up and player_hitbox.colliderect(clyde.rect)
                    and eaten_ghosts[3] and not clyde.dead):
                # Check if player has lives left
                if lives > 0:
                    # Subtract one live
                    lives -= 1

                    # Reset Pac-Man and Ghosts
                    (player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts) = reset(
                        player_x, player_y, player_direction,
                        direction_command, startup_counter, power_up,
                        power_counter,
                        blinky_x, blinky_y, blinky_direction, blinky_dead,
                        inky_x, inky_y, inky_direction, inky_dead,
                        pinky_x, pinky_y, pinky_direction, pinky_dead,
                        clyde_x, clyde_y, clyde_direction, clyde_dead,
                        eaten_ghosts)
                else:
                    game_over = True
                    player_moving = False
                    startup_counter = 0

            # Power Up is Active and collide with Blinky
            if (power_up and player_hitbox.colliderect(blinky.rect)
                    and not blinky.dead and not eaten_ghosts[0]):
                # Play eaten ghost sound once
                if enable_eat_ghost_snd:
                    eat_ghost_snd.play(loops=-1)
                    enable_eat_ghost_snd = False
                blinky_dead = True
                eaten_ghosts[0] = True
                score += (2 ** eaten_ghosts.count(True)) * 100

            # Power Up is Active and collide with Inky
            if (power_up and player_hitbox.colliderect(inky.rect)
                    and not inky.dead and not eaten_ghosts[1]):
                # Play eaten ghost sound once
                if enable_eat_ghost_snd:
                    eat_ghost_snd.play(loops=-1)
                    enable_eat_ghost_snd = False
                inky_dead = True
                eaten_ghosts[1] = True
                score += (2 ** eaten_ghosts.count(True)) * 100

            # Power Up is Active and collide with Pinky
            if (power_up and player_hitbox.colliderect(pinky.rect)
                    and not pinky.dead and not eaten_ghosts[2]):
                # Play eaten ghost sound once
                if enable_eat_ghost_snd:
                    eat_ghost_snd.play(loops=-1)
                    enable_eat_ghost_snd = False
                pinky_dead = True
                eaten_ghosts[2] = True
                score += (2 ** eaten_ghosts.count(True)) * 100

            # Power Up is Active and collide with Clyde
            if (power_up and player_hitbox.colliderect(clyde.rect)
                    and not clyde.dead and not eaten_ghosts[3]):
                # Play eaten ghost sound once
                if enable_eat_ghost_snd:
                    eat_ghost_snd.play(loops=-1)
                    enable_eat_ghost_snd = False
                clyde_dead = True
                eaten_ghosts[3] = True
                score += (2 ** eaten_ghosts.count(True)) * 100

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # If key is pressed
                # (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                if event.type == pygame.KEYDOWN:
                    # Exit when Escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_RIGHT:
                        direction_command = 0
                    if event.key == pygame.K_LEFT:
                        direction_command = 1
                    if event.key == pygame.K_UP:
                        direction_command = 2
                    if event.key == pygame.K_DOWN:
                        direction_command = 3
                    if event.key == pygame.K_SPACE and (game_over or game_won):
                        # Reset counter
                        startup_counter = 0
                        power_up = False
                        power_counter = 0
                        score = 0
                        lives = 3
                        game_won = False
                        game_over = False
                        level = copy.deepcopy(boards)

                        # Reset Player position
                        player_x = (WIDTH // 2) + x_offset
                        player_y = 663 + y_offset
                        player_direction = 0
                        direction_command = 0

                        # Reset Ghost positions
                        blinky_x = 56 + x_offset
                        blinky_y = 58 + y_offset
                        blinky_direction = 0

                        inky_x = 440 + x_offset
                        inky_y = 388 + y_offset
                        inky_direction = 2

                        pinky_x = 440 + x_offset
                        pinky_y = 438 + y_offset
                        pinky_direction = 2

                        clyde_x = 440 + x_offset
                        clyde_y = 438 + y_offset
                        clyde_direction = 2

                        # Reset Eaten Ghosts
                        eaten_ghosts = [False, False, False, False]

                        # Reset Ghost Dead
                        blinky_dead = False
                        pinky_dead = False
                        inky_dead = False
                        clyde_dead = False

                # If key is released
                if event.type == pygame.KEYUP:
                    # If key released and movement was the same
                    # player_direction then continue player_direction
                    # (0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN)
                    if event.key == pygame.K_RIGHT and direction_command == 0:
                        direction_command = player_direction
                    if event.key == pygame.K_LEFT and direction_command == 1:
                        direction_command = player_direction
                    if event.key == pygame.K_UP and direction_command == 2:
                        direction_command = player_direction
                    if event.key == pygame.K_DOWN and direction_command == 3:
                        direction_command = player_direction

            # Change player_direction if alowed to RIGHT
            if direction_command == 0 and turns_alowed[0]:
                player_direction = 0
            # Change player_direction if alowed to LEFT
            if direction_command == 1 and turns_alowed[1]:
                player_direction = 1
            # Change player_direction if alowed to UP
            if direction_command == 2 and turns_alowed[2]:
                player_direction = 2
            # Change player_direction if alowed to DOWN
            if direction_command == 3 and turns_alowed[3]:
                player_direction = 3

            # If player moves from board place it at opposite side
            # If player moves from Right side of board then appear Left
            if player_x > WIDTH + x_offset:
                player_x = - 47 + x_offset
            # If player moves from Left side of board then appear Right
            elif player_x < - 50 + x_offset:
                player_x = WIDTH - 3 + x_offset

            if blinky.in_box and blinky_dead:
                blinky_dead = False
                # Stop eaten_ghost Sound
                eat_ghost_snd.stop()
                # Reset eaten_ghost sound
                enable_eat_ghost_snd = True
            if inky.in_box and inky_dead:
                inky_dead = False
                # Stop eaten_ghost Sound
                eat_ghost_snd.stop()
                # Reset eaten_ghost sound
                enable_eat_ghost_snd = True
            if pinky.in_box and pinky_dead:
                pinky_dead = False
                # Stop eaten_ghost Sound
                eat_ghost_snd.stop()
                # Reset eaten_ghost sound
                enable_eat_ghost_snd = True
            if clyde.in_box and clyde_dead:
                clyde_dead = False
                # Stop eaten_ghost Sound
                eat_ghost_snd.stop()
                # Reset eaten_ghost sound
                enable_eat_ghost_snd = True

            # Update screen
            pygame.display.flip()

        # Quit Game
        pygame.display.quit()
