# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/main.py
# INFO: Enigma Encoder / Decoder for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 17-04-2023
# Last update: 26-04-2023
# Github: https://github.com/M4R1N447/Mr.-Robot-Escape-Game-Briefcase
# Status: In Progress
# __________________________________________________

'''
ENIGMA DETAILS:
SIMULATOR: http://mckoss.com/enigma-simulator-js/
DOCUMENTATION: https://mckoss.com/posts/paper-enigma/


HISTORICAL ROTOR DETAILS
Rotor Details:  https://en.wikipedia.org/wiki/Enigma_rotor_details

ROTOR WIRING:

Rotor I:    EKMFLGDQVZNTOWYHXUSPAIBRCJ (1930) - Enigma I
Rotor II:   AJDKSIRUXBLHWTMCQGZNPYFVOE (1930) - Enigma I
Rotor III:  BDFHJLCPRTXVZNYEIWGAKMUSQO (1930) - Enigma I
Rotor IV:   ESOVPZJAYQUIRHXLNFTGKDCMWB December (1938) - M3 Army
Rotor V:    VZBRGITYUPSDNHLXAWMJQOFECK December (1938) - M3 Army

NOTCH POSITIONS:

Rotor I:    Q - If rotor steps from Q to R, the next rotor is advanced
Rotor II:   E - If rotor steps from E to F, the next rotor is advanced
Rotor III:  V - If rotor steps from V to W, the next rotor is advanced
Rotor IV:   J - If rotor steps from J to K, the next rotor is advanced
Rotor V:    Z - If rotor steps from Z to A, the next rotor is advanced

REFLECTORS:

Reflector A:    EJMZALYXVBWFCRQUONTSPIKHGD
Reflector B:    YRUHQSLDPXNGOKMIEBFZCWVJAT
Reflector C:    FVPJIAOYEDRZXWGCTKUQSBNMHL

# Some challenge stuff which can be used for game
https://www.ciphermachinesandcryptology.com/nl/challenge.htm#s1

'''

# Imports
import pygame
from pygame import mixer
from pygame.locals import FULLSCREEN

from sound import Sound as Sound

from key_board import Key_board
from plug_board import Plug_board
from rotor import Rotor
from reflector import Reflector
from machine import Enigma

# Config Color Settings
from config import DARK_PURPLE as BG_COLOR
from config import MEDIUM_PURPLE as BG_MACHINE_COLOR

from config import DARK_GREEN as BORDER_COLOR
from config import EXTRA_LIGHT_PURPLE as BUFFER_BORDER_COLOR
from config import EXTRA_LIGHT_PURPLE as CONFIG_INACTIVE_COLOR
from config import LIGHT_GREEN as CONFIG_ACTIVE_COLOR

from config import STANDARD_FONT_COLOR as STANDARD_FONT_COLOR
from config import EXTRA_LIGHT_GREEN as INPUT_TXT_COLOR
from config import RED as OUTPUT_TXT_COLOR
from config import LIGHT_BLUE as MESSAGE_TXT_COLOR

from config import LIGHT_GREEN as output_line_1_TXT_COLOR
from config import MEDIUM_GREEN as output_line_2_TXT_COLOR
from config import MEDIUM_GREEN as output_line_3_TXT_COLOR
from config import MEDIUM_GREEN as output_line_4_TXT_COLOR
from config import MEDIUM_GREEN as output_line_5_TXT_COLOR

from config import LIGHT_GREEN as COUNTER_TXT_COLOR
from config import LIGHT_GREEN as INPUT_BOX_TXT_COLOR

# Briefcase Screen Settings
from config import SCREEN_WIDTH as WIDTH
from config import SCREEN_HEIGHT as HEIGHT

# Fonts
from config import FONT_PATH as FONT_PATH
from config import HEADER_FONT as HEADER_FONT

# Audio
from config import ENIGMA_SHORT_CLK_SND as SHORT_CLK_SND
from config import ENIGMA_MEDIUM_CLK_SND as MEDIUM_CLK_SND
from config import ENIGMA_LONG_CLK_SND as LONG_CLK_SND


# Game Class
class Game:
    def __init__(self, max_score=0, difficulty=0, complexity=None,
                 game_input=None, hints=None, solution=None):
        self.max_score = max_score
        self.difficulty = difficulty
        self.complexity = complexity
        self.game_input = game_input
        self.hints = hints
        self.solution = solution

    # Get game difficulty from Puzzle_data Class
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    # Get game difficulty from Puzzle_data Class
    def set_solution(self, solution):
        self.solution = solution

    # Set Game Hints
    def game_hints(self):
        if self.difficulty == 1:
            self.hints = []
        elif self.difficulty == 2:
            self.hints = []
        elif self.difficulty == 3:
            self.hints = []
        return self.hints

    # Game Intro Screen
    def game_intro_screen(self):
        print()
        print("--------------------------------------------")
        print("           E N I G M A    T O O L           ")
        print()
        print("--------------------------------------------")
        print()

    # Main Game
    def game_play(self):

        # Initlialize Pygame
        pygame.init()

        # - S O U N D S   A N D   M U S I C - #

        # Define Enigma Sound Files
        kb_short_clk_snd = Sound(SHORT_CLK_SND, 0.6, 0, 0)
        kb_medium_clk_snd = Sound(MEDIUM_CLK_SND, 0.6, 0, 0)
        kb_long_clk_snd = Sound(LONG_CLK_SND, 0.6, 0, 0)

        # Initialize Timer
        timer = pygame.time.Clock()
        fps = 60

        # Define fonts
        NORMAL_FONT = pygame.font.SysFont("FreeMono", 20, bold=True)
        CONFIG_FONT = pygame.font.SysFont("FreeMono", 18, bold=True)
        SMALL_CONFIG_FONT = pygame.font.SysFont("FreeMono", 12, bold=True)
        SMALL_FONT = pygame.font.SysFont("FreeMono", 14, bold=True)
        TITLE_FONT = pygame.font.Font((FONT_PATH + HEADER_FONT + ".ttf"), 72)

        # Current Screen Width & Height
        screeninfo = pygame.display.Info()
        SCREEN_WIDTH = screeninfo.current_w
        SCREEN_HEIGHT = screeninfo.current_h

        # Calculate left margin to center the game on screen
        LEFT_MARGIN = (SCREEN_WIDTH - WIDTH) / 2
        HOR_CENTER = SCREEN_WIDTH / 2

        # Fullscreen without menu and borders
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        MARGINS = {"top": 275, "bottom": 100, "left": LEFT_MARGIN,  "right": 0}

        # Initialize Variables
        self.INPUT = ""
        self.OUTPUT = ""
        self.output_line_1 = ""
        self.output_line_2 = ""
        self.output_line_3 = ""
        self.output_line_4 = ""
        self.output_line_5 = ""
        letter_combination = ""
        used_letters = ""

        TITLE_HEIGHT = 650
        gap = 75
        max_chars = 70
        key = "ABC"
        self.message = ""

        ring = (1, 1, 1)

        self.PATH = []
        new_plugboard_config = []
        cfg_plugboard = ["AX", "DQ", "EF", "RH", "NY", "MK", "WC", "BG", "TV", "ZI"]

        # Ignored keyboard inputs
        ignore_list = (
            pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_LSHIFT, pygame.K_RSHIFT,
            pygame.K_LCTRL, pygame.K_RCTRL,
            pygame.K_LALT, pygame.K_RALT,
            pygame.K_CAPSLOCK, pygame.K_TAB,
            pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7,
            pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12, pygame.K_F13, pygame.K_F14, pygame.K_F15
            )

        # - M A C H I N E   H A R D W A R E   S E T T I N G S - #

        # Define Keyboard and Plugboard wiring
        keyboard = Key_board()
        plugboard = Plug_board(cfg_plugboard)

        # Define Historical Enigma Rotor wiring and Notch
        rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
        rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
        rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
        rotor_IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
        rotor_V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")

        # Define Historical Enigma Reflectors wiring
        reflector_A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
        reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        reflector_C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

        # Initial machine configuration
        self.reflector = reflector_A
        self.left_rotor = rotor_I
        self.middle_rotor = rotor_II
        self.right_rotor = rotor_III
        self.plugboard = plugboard
        self.keyboard = keyboard
        self.ring = ring
        self.key = key

        def show_machine_configuration():
            print("---------------------")
            print("MACHINE CONFIGURATION")
            print("---------------------")
            print(f"LEFT ROTOR: {self.cfg_rotor_l}")
            print(f"MIDDLE ROTOR: {self.cfg_rotor_m}")
            print(f"RIGHT ROTOR: {self.cfg_rotor_r}")
            print(f"REFLECTOR: {self.cfg_reflector}")
            print(f"PLUGBOARD: {cfg_plugboard}")
            print(f"KEY: {self.key}")
            print(f"RING: {self.ring}")
            print("---------------------")
            print("")

        # Define Enigma Configuration
        def enigma_reconfig(self, plugboard, left_rotor, middle_rotor, right_rotor, reflector, ring, key):

            # Define Historical Enigma Rotor wiring and Notch
            reset_rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
            reset_rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
            reset_rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
            reset_rotor_IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
            reset_rotor_V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")

            # Define Historical Enigma Reflectors wiring
            reset_reflector_A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
            reset_reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
            reset_reflector_C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

            # Set Left rotor in initial position
            if self.left_rotor == rotor_I:
                left_rotor = reset_rotor_I
            elif self.left_rotor == rotor_II:
                left_rotor = reset_rotor_II
            elif self.left_rotor == rotor_III:
                left_rotor = reset_rotor_III
            elif self.left_rotor == rotor_IV:
                left_rotor = reset_rotor_IV
            elif self.left_rotor == rotor_V:
                left_rotor = reset_rotor_V

            # Set Middle rotor in initial position
            if self.middle_rotor == rotor_I:
                middle_rotor = reset_rotor_I
            elif self.middle_rotor == rotor_II:
                middle_rotor = reset_rotor_II
            elif self.middle_rotor == rotor_III:
                middle_rotor = reset_rotor_III
            elif self.middle_rotor == rotor_IV:
                middle_rotor = reset_rotor_IV
            elif self.middle_rotor == rotor_V:
                middle_rotor = reset_rotor_V

            # Set Right rotor in initial position
            if self.right_rotor == rotor_I:
                right_rotor = reset_rotor_I
            elif self.right_rotor == rotor_II:
                right_rotor = reset_rotor_II
            elif self.right_rotor == rotor_III:
                right_rotor = reset_rotor_III
            elif self.right_rotor == rotor_IV:
                right_rotor = reset_rotor_IV
            elif self.right_rotor == rotor_V:
                right_rotor = reset_rotor_V

            # Set Reflector in initial position
            if self.reflector == reflector_A:
                reflector = reset_reflector_A
            elif self.reflector == reflector_B:
                reflector = reset_reflector_B
            elif self.reflector == reflector_C:
                reflector = reset_reflector_C

            self.ENIGMA = Enigma(reflector,
                                 left_rotor,
                                 middle_rotor,
                                 right_rotor,
                                 plugboard,
                                 self.keyboard,
                                 )
            # Set the rotor rings (notch position)
            self.ENIGMA.set_ring(ring)

            # Set the offset key for each rotor (each letter for a rotor)
            self.ENIGMA.set_key(key)

        # Reset Machine to default state
        def reset_machine(self):
            self.INPUT = ""
            self.OUTPUT = ""
            self.PATH = []
            self.message = ""

            # Reconfig the Enigma Machine
            enigma_reconfig(self, self.plugboard, self.left_rotor, self.middle_rotor, self.right_rotor,
                            self.reflector, self.ring, self.key)

            # Show machine configuration in terminal
            # show_machine_configuration()

        # Shift output line downwards on each linefeed
        def line_feed(self):
            # Fill output line 5 with output line 4 when it has data
            if self.output_line_4 != "":
                self.output_line_5 = self.output_line_4
            else:
                self.output_line_5 = ""
            # Fill output line 4 with output line 3 when it has data
            if self.output_line_3 != "":
                self.output_line_4 = self.output_line_3
            else:
                self.output_line_4 = ""
            # Fill output line 3 with output line 2 when it has data
            if self.output_line_2 != "":
                self.output_line_3 = self.output_line_2
            else:
                self.output_line_3 = ""
            # Fill output line 2 with output line 1 when it has data
            if self.output_line_1 != "":
                self.output_line_2 = self.output_line_1
            else:
                self.output_line_2 = ""
            # Send data to output line 1 when pressed enter
            self.output_line_1 = self.OUTPUT

        # Reflector type
        def reflector_type():
            if self.reflector is reflector_A:
                self.cfg_reflector = "A"
            elif self.reflector is reflector_B:
                self.cfg_reflector = "B"
            elif self.reflector is reflector_C:
                self.cfg_reflector = "C"
            return self.cfg_reflector

        # Left Rotor type
        def left_rotor_type():
            if self.left_rotor == rotor_I:
                self.cfg_rotor_l = "1"
            elif self.left_rotor == rotor_II:
                self.cfg_rotor_l = "2"
            elif self.left_rotor == rotor_III:
                self.cfg_rotor_l = "3"
            elif self.left_rotor == rotor_IV:
                self.cfg_rotor_l = "4"
            elif self.left_rotor == rotor_V:
                self.cfg_rotor_l = "5"
            return self.cfg_rotor_l

        # Middle Rotor type
        def middle_rotor_type():
            if self.middle_rotor == rotor_I:
                self.cfg_rotor_m = "1"
            elif self.middle_rotor == rotor_II:
                self.cfg_rotor_m = "2"
            elif self.middle_rotor == rotor_III:
                self.cfg_rotor_m = "3"
            elif self.middle_rotor == rotor_IV:
                self.cfg_rotor_m = "4"
            elif self.middle_rotor == rotor_V:
                self.cfg_rotor_m = "5"
            return self.cfg_rotor_m

        # Right Rotor type
        def right_rotor_type():
            if self.right_rotor == rotor_I:
                self.cfg_rotor_r = "1"
            elif self.right_rotor == rotor_II:
                self.cfg_rotor_r = "2"
            elif self.right_rotor == rotor_III:
                self.cfg_rotor_r = "3"
            elif self.right_rotor == rotor_IV:
                self.cfg_rotor_r = "4"
            elif self.right_rotor == rotor_V:
                self.cfg_rotor_r = "5"
            return self.cfg_rotor_r

        # Key config variables
        self.cfg_key_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_key_active = False
        self.cfg_key = self.key

        # Reflector config variables
        self.cfg_reflector_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_reflector_active = False
        reflector_type()

        # Left Rotor config variables
        self.cfg_rotor_l_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_rotor_l_active = False
        left_rotor_type()

        # Middle Rotor config variables
        self.cfg_rotor_m_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_rotor_m_active = False
        middle_rotor_type()

        # Right Rotor config variables
        self.cfg_rotor_r_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_rotor_r_active = False
        right_rotor_type()

        # Left Ring config variables
        self.cfg_ring_l_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_ring_l_active = False
        self.cfg_ring_l = str(ring[0])

        # Middle Ring config variables
        self.cfg_ring_m_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_ring_m_active = False
        self.cfg_ring_m = str(ring[1])

        # Right Ring config variables
        self.cfg_ring_r_border_color = CONFIG_INACTIVE_COLOR
        self.cfg_ring_r_active = False
        self.cfg_ring_r = str(ring[2])

        # Plugboard config variables
        cfg_plugboard_border_color = CONFIG_INACTIVE_COLOR
        cfg_plugboard_active = False

        # Set Enigma with initial machine configuration
        self.ENIGMA = Enigma(self.reflector,
                             self.left_rotor,
                             self.middle_rotor,
                             self.right_rotor,
                             self.plugboard,
                             self.keyboard,
                             )
        # Set the rotor rings (notch position)
        self.ENIGMA.set_ring(self.ring)

        # Set the offset key for each rotor (each letter for a rotor)
        self.ENIGMA.set_key(self.key)

        # - R E N D E R   D Y N A M I C   S C R E E N   E L E M E N T S - #

        def draw_machine(self):
            # Background
            SCREEN.fill(BG_COLOR)

            # Config Background and Border (X, Y, WIDTH, HEIGHT)
            bg_config.fill(BG_MACHINE_COLOR, config_rect)
            pygame.draw.rect(SCREEN, BORDER_COLOR, config_border, width=3, border_radius=7)

            # Plugboard Config Background and Border (X, Y, WIDTH, HEIGHT)
            plugboard_config.fill(BG_MACHINE_COLOR, plugboard_config_rect)
            pygame.draw.rect(SCREEN, cfg_plugboard_border_color, plugboard_config_border, width=1, border_radius=7)

            # Machine Background and Border (X, Y, WIDTH, HEIGHT)
            bg_machine.fill(BG_MACHINE_COLOR, machine_rect)
            pygame.draw.rect(SCREEN, BORDER_COLOR, machine_border, width=3, border_radius=7)

            # Draw Input / Output Background and Border (X, Y, WIDTH, HEIGHT)
            bg_in_out.fill(BG_COLOR, in_out)
            pygame.draw.rect(SCREEN, BORDER_COLOR, in_out_border, width=3, border_radius=7)

            # Output Window Background and Border (X, Y, WIDTH, HEIGHT)
            bg_output_window.fill(BG_MACHINE_COLOR, output_window)
            pygame.draw.rect(SCREEN, BUFFER_BORDER_COLOR, output_window_border, width=1, border_radius=15)

            # Screen Title
            SCREEN.blit(title_render, title_rect)

            # Machine Configuration Title
            SCREEN.blit(machine_config_render, machine_config_rect)

            # Enigma Image
            SCREEN.blit(enigma_image, enigma_image_rect)

            # Draw Enigma Machine and Signal Paths
            self.ENIGMA.draw(self.PATH, SCREEN, WIDTH + MARGINS["left"], HEIGHT, MARGINS, gap, NORMAL_FONT)

            # Draw Player Message
            message_text = SMALL_FONT.render(self.message, True, MESSAGE_TXT_COLOR)
            message_text_box = message_text.get_rect(center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 - 35) + TITLE_HEIGHT))
            SCREEN.blit(message_text, message_text_box)

            # Draw Input Text
            input_text = NORMAL_FONT.render(self.INPUT, True, INPUT_TXT_COLOR)
            input_text_box = input_text.get_rect(center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3) + TITLE_HEIGHT))
            SCREEN.blit(input_text, input_text_box)

            #  Draw Output Text
            output_text = NORMAL_FONT.render(self.OUTPUT, True, OUTPUT_TXT_COLOR)
            output_text_box = output_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + 30) + TITLE_HEIGHT))
            SCREEN.blit(output_text, output_text_box)

            # Output Line 1
            output_line_1_text = NORMAL_FONT.render(self.output_line_1, True, output_line_1_TXT_COLOR)
            output_line_1_text_box = output_line_1_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + (60) + TITLE_HEIGHT)))
            SCREEN.blit(output_line_1_text, output_line_1_text_box)

            # Output Line 2
            output_line_2_text = NORMAL_FONT.render(self.output_line_2, True, output_line_2_TXT_COLOR)
            output_line_2_text_box = output_line_2_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + (90) + TITLE_HEIGHT)))
            SCREEN.blit(output_line_2_text, output_line_2_text_box)

            # Output Line 3
            output_line_3_text = NORMAL_FONT.render(self.output_line_3, True, output_line_3_TXT_COLOR)
            output_line_3_text_box = output_line_3_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + (120) + TITLE_HEIGHT)))
            SCREEN.blit(output_line_3_text, output_line_3_text_box)

            # Output Line 4
            output_line_4_text = NORMAL_FONT.render(self.output_line_4, True, output_line_4_TXT_COLOR)
            output_line_4_text_box = output_line_4_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + (150) + TITLE_HEIGHT)))
            SCREEN.blit(output_line_4_text, output_line_4_text_box)

            # Output Line 5
            output_line_5_text = NORMAL_FONT.render(self.output_line_5, True, output_line_5_TXT_COLOR)
            output_line_5_text_box = output_line_5_text.get_rect(
                center=((WIDTH + (MARGINS["left"])*2) / 2, (MARGINS["top"] / 3 + (180) + TITLE_HEIGHT)))
            SCREEN.blit(output_line_5_text, output_line_5_text_box)

            # Character Counter
            counter = max_chars - len(self.INPUT)
            counter_text = SMALL_FONT.render(f"NEW LINEFEED IN {counter} CHARACTERS", True, COUNTER_TXT_COLOR)
            counter_text_box = counter_text.get_rect(
                center=((WIDTH + ((MARGINS["left"])*2)+630) / 2, (MARGINS["top"] / 3 + (205) + TITLE_HEIGHT)))
            SCREEN.blit(counter_text, counter_text_box)

            # K E Y   C O N F I G

            # New Key Title
            SCREEN.blit(self.cfg_key_render1, self.cfg_key_rect1)
            SCREEN.blit(self.cfg_key_render2, self.cfg_key_rect2)

            # New Key Input Box
            key_input_box = CONFIG_FONT.render(self.cfg_key, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_key_border_color, self.cfg_key_input_box, width=1, border_radius=7)
            SCREEN.blit(key_input_box, (self.cfg_key_input_box.x+8, self.cfg_key_input_box.y+1))

            # R E F L E C T O R   C O N F I G

            # New Reflector Title
            SCREEN.blit(self.cfg_reflector_render1, self.cfg_reflector_rect1)
            SCREEN.blit(self.cfg_reflector_render2, self.cfg_reflector_rect2)

            # New Reflector Input Box
            reflector_input_box = CONFIG_FONT.render(self.cfg_reflector, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_reflector_border_color, self.cfg_reflector_input_box, width=1, border_radius=7)
            SCREEN.blit(reflector_input_box, (self.cfg_reflector_input_box.x+17, self.cfg_reflector_input_box.y+1))

            # L E F T   R O T O R / R I N G   C O N F I G

            # New Rotor Left Title
            SCREEN.blit(self.cfg_rotor_l_render1, self.cfg_rotor_l_rect1)
            SCREEN.blit(self.cfg_rotor_l_render2, self.cfg_rotor_l_rect2)

            # New Rotor Left Input Box
            rotor_l_input_box = CONFIG_FONT.render(self.cfg_rotor_l, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_rotor_l_border_color, self.cfg_rotor_l_input_box, width=1, border_radius=7)
            SCREEN.blit(rotor_l_input_box, (self.cfg_rotor_l_input_box.x+17, self.cfg_rotor_l_input_box.y+1))

            # New Ring Left Input Box
            ring_l_input_box = CONFIG_FONT.render(self.cfg_ring_l, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_ring_l_border_color, self.cfg_ring_l_input_box, width=1, border_radius=7)
            SCREEN.blit(ring_l_input_box, (self.cfg_ring_l_input_box.x+17, self.cfg_ring_l_input_box.y+1))

            # M I D D L E   R O T O R / R I N G   C O N F I G

            # New Rotor Middle Title
            SCREEN.blit(self.cfg_rotor_m_render1, self.cfg_rotor_m_rect1)
            SCREEN.blit(self.cfg_rotor_m_render2, self.cfg_rotor_m_rect2)

            # New Rotor Middle Input Box
            rotor_m_input_box = CONFIG_FONT.render(self.cfg_rotor_m, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_rotor_m_border_color, self.cfg_rotor_m_input_box, width=1, border_radius=7)
            SCREEN.blit(rotor_m_input_box, (self.cfg_rotor_m_input_box.x+17, self.cfg_rotor_m_input_box.y+1))

            # New Ring Middle Input Box
            ring_m_input_box = CONFIG_FONT.render(self.cfg_ring_m, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_ring_m_border_color, self.cfg_ring_m_input_box, width=1, border_radius=7)
            SCREEN.blit(ring_m_input_box, (self.cfg_ring_m_input_box.x+17, self.cfg_ring_m_input_box.y+1))

            # R I G H T   R O T O R / R I N G   C O N F I G

            # New Rotor Right Title
            SCREEN.blit(self.cfg_rotor_r_render1, self.cfg_rotor_r_rect1)
            SCREEN.blit(self.cfg_rotor_r_render2, self.cfg_rotor_r_rect2)

            # New Rotor Right Input Box
            rotor_r_input_box = CONFIG_FONT.render(self.cfg_rotor_r, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_rotor_r_border_color, self.cfg_rotor_r_input_box, width=1, border_radius=7)
            SCREEN.blit(rotor_r_input_box, (self.cfg_rotor_r_input_box.x+17, self.cfg_rotor_r_input_box.y+1))

            # New Ring Right Input Box
            ring_r_input_box = CONFIG_FONT.render(self.cfg_ring_r, True, INPUT_BOX_TXT_COLOR)
            pygame.draw.rect(SCREEN, self.cfg_ring_r_border_color, self.cfg_ring_r_input_box, width=1, border_radius=7)
            SCREEN.blit(ring_r_input_box, (self.cfg_ring_r_input_box.x+17, self.cfg_ring_r_input_box.y+1))

            # P L U G B O A R D   C O N F I G

            # New Plugboard Input Box
            # Convert each list item from cfg_plugboard in a string and join them seperated by a space
            plugboard_text = " ".join(map(str, cfg_plugboard))
            plugboard_input = CONFIG_FONT.render(plugboard_text, True, INPUT_BOX_TXT_COLOR)
            cfg_plugboard_rect = plugboard_input.get_rect(center=(HOR_CENTER + 340, 212))

            # New Plugboard Title
            SCREEN.blit(cfg_plugboard_render1, cfg_plugboard_rect1)
            SCREEN.blit(cfg_plugboard_render2, cfg_plugboard_rect2)
            SCREEN.blit(plugboard_input, cfg_plugboard_rect)

        # Config Background and Border (X, Y, WIDTH, HEIGHT)
        bg_config = pygame.display.get_surface()
        config_rect = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 524, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 599, 1048, 83)
        config_border = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 525, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 600, 1050, 85)

        # Plugboard Config Background and Border (X, Y, WIDTH, HEIGHT)
        plugboard_config = pygame.display.get_surface()
        plugboard_config_rect = pygame.Rect(HOR_CENTER + 170, 201, 343, 20)
        plugboard_config_border = pygame.Rect(HOR_CENTER + 170, 201, 343, 20)
        # plugboard_config_rect = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) + 170, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 343, 20)
        # plugboard_config_border = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) + 170, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 343, 20)

        # Plugboard Title
        cfg_plugboard_render1 = (SMALL_CONFIG_FONT.render("PLUGBOARD", True, INPUT_BOX_TXT_COLOR))
        cfg_plugboard_rect1 = cfg_plugboard_render1.get_rect(center=(HOR_CENTER + 340, 186))
        cfg_plugboard_render2 = (SMALL_CONFIG_FONT.render("CONNECTIONS", True, INPUT_BOX_TXT_COLOR))
        cfg_plugboard_rect2 = cfg_plugboard_render2.get_rect(center=(HOR_CENTER + 340, 196))

        # cfg_plugboard_rect = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) + 170, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 343, 20)

        # Machine Background and Border (X, Y, WIDTH, HEIGHT)
        bg_machine = pygame.display.get_surface()
        machine_rect = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 524, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 499, 1048, 448)
        machine_border = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 525, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 500, 1050, 450)

        # Draw Input / Output Background and Border (X, Y, WIDTH, HEIGHT)
        bg_in_out = pygame.display.get_surface()
        in_out = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 474, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 19, 948, 238)
        in_out_border = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 475, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 20, 950, 240)

        # Output Window Background and Border (X, Y, WIDTH, HEIGHT)
        bg_output_window = pygame.display.get_surface()
        output_window = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 439, ((MARGINS["top"] / 3) + TITLE_HEIGHT) + 46, 878, 145)
        output_window_border = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 440, ((MARGINS["top"] / 3) + TITLE_HEIGHT) + 45, 880, 147)

        # Screen Title
        title_text = "- E N I G M A -"
        title_render = (TITLE_FONT.render(title_text, True, STANDARD_FONT_COLOR))
        title_rect = title_render.get_rect(center=(HOR_CENTER, 75))

        # Enigma Image
        enigma_image = pygame.image.load("P:/game/Briefcase Pi 3B/Enigma/enigma2.png")
        enigma_image = pygame.transform.scale(enigma_image, (2000 // 5, 2500 // 5))
        enigma_image_rect = enigma_image.get_rect(center=(SCREEN_WIDTH/2 + 700, 450))

        # Machine Configuration Title
        machine_config_title = "M A C H I N E   C O N F I G U R A T I O N"
        machine_config_render = (NORMAL_FONT.render(machine_config_title, True, INPUT_BOX_TXT_COLOR))
        machine_config_rect = machine_config_render.get_rect(center=(HOR_CENTER, 160))

        # Key Config
        self.cfg_key_render1 = (SMALL_CONFIG_FONT.render("KEY", True, INPUT_BOX_TXT_COLOR))
        self.cfg_key_rect1 = self.cfg_key_render1.get_rect(center=(HOR_CENTER - 490, 186))
        self.cfg_key_render2 = (SMALL_CONFIG_FONT.render("SETTINGS", True, INPUT_BOX_TXT_COLOR))
        self.cfg_key_rect2 = self.cfg_key_render2.get_rect(center=(HOR_CENTER - 490, 196))
        self.cfg_key_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 514, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 50, 20)

        # Reflector Config
        self.cfg_reflector_render1 = (SMALL_CONFIG_FONT.render("REFLECTOR", True, INPUT_BOX_TXT_COLOR))
        self.cfg_reflector_rect1 = self.cfg_reflector_render1.get_rect(center=(HOR_CENTER - 390, 186))
        self.cfg_reflector_render2 = (SMALL_CONFIG_FONT.render("TYPE", True, INPUT_BOX_TXT_COLOR))
        self.cfg_reflector_rect2 = self.cfg_reflector_render2.get_rect(center=(HOR_CENTER - 390, 196))
        self.cfg_reflector_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 414, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 50, 20)

        # Left Rotor|Ring Config
        self.cfg_rotor_l_render1 = (SMALL_CONFIG_FONT.render("LEFT", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_l_rect1 = self.cfg_rotor_l_render1.get_rect(center=(HOR_CENTER - 270, 186))
        self.cfg_rotor_l_render2 = (SMALL_CONFIG_FONT.render("ROTOR  RING", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_l_rect2 = self.cfg_rotor_l_render2.get_rect(center=(HOR_CENTER - 273, 196))
        self.cfg_rotor_l_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 320, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)
        self.cfg_ring_l_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 270, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)

        # Middle Rotor|Ring Config
        self.cfg_rotor_m_render1 = (SMALL_CONFIG_FONT.render("MIDDLE", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_m_rect1 = self.cfg_rotor_m_render1.get_rect(center=(HOR_CENTER - 87, 186))
        self.cfg_rotor_m_render2 = (SMALL_CONFIG_FONT.render("ROTOR  RING", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_m_rect2 = self.cfg_rotor_m_render2.get_rect(center=(HOR_CENTER - 90, 196))
        self.cfg_rotor_m_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 137, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)
        self.cfg_ring_m_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) - 87, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)

        # Right Rotor|Ring Config
        self.cfg_rotor_r_render1 = (SMALL_CONFIG_FONT.render("RIGHT", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_r_rect1 = self.cfg_rotor_r_render1.get_rect(center=(HOR_CENTER + 94, 186))
        self.cfg_rotor_r_render2 = (SMALL_CONFIG_FONT.render("ROTOR  RING", True, INPUT_BOX_TXT_COLOR))
        self.cfg_rotor_r_rect2 = self.cfg_rotor_r_render2.get_rect(center=(HOR_CENTER + 91, 196))
        self.cfg_rotor_r_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) + 44, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)
        self.cfg_ring_r_input_box = pygame.Rect(((WIDTH + (MARGINS["left"])*2) / 2) + 94, ((MARGINS["top"] / 3) + TITLE_HEIGHT) - 540, 45, 20)

        # Main Loop
        run = True
        while run:
            # Set framerate
            timer.tick(fps)

            # - T R I G G E R E D   E V E N T S - #
            for event in pygame.event.get():

                # Stop program when user exits screen
                if event.type == pygame.QUIT:
                    run = False

                # Get keyboard inputs
                if event.type == pygame.KEYDOWN:

                    #   K E Y   C O N F I G   #
                    if self.cfg_key_active:
                        keyboard_input = event.unicode
                        # Reset entry to last value
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            self.cfg_key = self.key
                        # Delete last char
                        elif event.key == pygame.K_BACKSPACE:
                            kb_long_clk_snd.play_sound()
                            self.cfg_key = self.cfg_key[:-1]
                        elif keyboard_input in "abcdefghijklmnopqrstuvwxyz":
                            kb_long_clk_snd.play_sound()
                            self.cfg_key += keyboard_input.upper()
                            # Set key to new value if input has 3 chars
                            if len(self.cfg_key) > 2:
                                self.key = self.cfg_key
                                # Reset machine with new key value
                                reset_machine(self)
                                # Toggle the active variable.
                                self.cfg_key_active = not self.cfg_key_active
                                # Set input box color active / inactive
                                self.cfg_key_border_color = CONFIG_ACTIVE_COLOR if self.cfg_key_active else CONFIG_INACTIVE_COLOR
                            else:
                                pass

                    #   R E F L E C T O R   C O N F I G   #
                    elif self.cfg_reflector_active:
                        keyboard_input = event.unicode
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            self.cfg_reflector = reflector_type()
                        elif keyboard_input in "abc":
                            kb_long_clk_snd.play_sound()
                            self.cfg_reflector = keyboard_input.upper()
                            if keyboard_input == "c":
                                self.reflector = reflector_C
                            elif keyboard_input == "b":
                                self.reflector = reflector_B
                            elif keyboard_input == "a":
                                self.reflector = reflector_A
                            # Reset machine with new reflector value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_reflector_active = not self.cfg_reflector_active
                            # Set input box color active / inactive
                            self.cfg_reflector_border_color = CONFIG_ACTIVE_COLOR if self.cfg_reflector_active else CONFIG_INACTIVE_COLOR
                        else:
                            self.cfg_reflector = reflector_type()

                    #   L E F T   R O T O R   C O N F I G   #
                    elif self.cfg_rotor_l_active:
                        keyboard_input = event.unicode
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_l = left_rotor_type()
                        elif keyboard_input in "12345":
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_l = keyboard_input
                            if keyboard_input == "1":
                                self.left_rotor = rotor_I
                            elif keyboard_input == "2":
                                self.left_rotor = rotor_II
                            elif keyboard_input == "3":
                                self.left_rotor = rotor_III
                            elif keyboard_input == "4":
                                self.left_rotor = rotor_IV
                            elif keyboard_input == "5":
                                self.left_rotor = rotor_V
                            # Reset machine with new rotor_l value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_rotor_l_active = not self.cfg_rotor_l_active
                            # Set input box color active / inactive
                            self.cfg_rotor_l_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_l_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #   L E F T   R I N G   C O N F I G   #
                    elif self.cfg_ring_l_active:
                        keyboard_input = event.unicode
                        if keyboard_input in "1234567890":
                            kb_long_clk_snd.play_sound()
                            self.cfg_ring_l += keyboard_input
                            # Convert from to list, edit value, convert back to tuple with integers
                            ring_config = list(self.ring)
                            ring_config[0] = self.cfg_ring_l
                            self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                            # Set key to new value if input has 2 chars
                            if len(self.cfg_ring_l) > 1:
                                # Convert from to list, edit value, convert back to tuple with integers
                                ring_config = list(self.ring)
                                ring_config[0] = self.cfg_ring_l
                                if int(ring_config[0]) > 26:
                                    ring_config[0] = 26
                                self.cfg_ring_l = str(ring_config[0])
                                self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                                # Reset machine with new ring value
                                reset_machine(self)
                                # Toggle the active variable.
                                self.cfg_ring_l_active = not self.cfg_ring_l_active
                                # Set input box color active / inactive
                                self.cfg_ring_l_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_l_active else CONFIG_INACTIVE_COLOR
                            else:
                                pass
                        elif event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            # Reset machine with new ring value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_ring_l_active = not self.cfg_ring_l_active
                            # Set input box color active / inactive
                            self.cfg_ring_l_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_l_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #  M I D D L E   R O T O R   C O N F I G   #
                    elif self.cfg_rotor_m_active:
                        keyboard_input = event.unicode
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_m = middle_rotor_type()
                        elif keyboard_input in "12345":
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_m = keyboard_input
                            if keyboard_input == "1":
                                self.middle_rotor = rotor_I
                            elif keyboard_input == "2":
                                self.middle_rotor = rotor_II
                            elif keyboard_input == "3":
                                self.middle_rotor = rotor_III
                            elif keyboard_input == "4":
                                self.middle_rotor = rotor_IV
                            elif keyboard_input == "5":
                                self.middle_rotor = rotor_V
                            # Reset machine with new rotor_m value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_rotor_m_active = not self.cfg_rotor_m_active
                            # Set input box color active / inactive
                            self.cfg_rotor_m_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_m_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #   M I D D L E   R I N G   C O N F I G   #
                    elif self.cfg_ring_m_active:
                        keyboard_input = event.unicode
                        if keyboard_input in "1234567890":
                            kb_long_clk_snd.play_sound()
                            self.cfg_ring_m += keyboard_input
                            # Convert from to list, edit value, convert back to tuple with integers
                            ring_config = list(self.ring)
                            ring_config[1] = self.cfg_ring_m
                            self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                            # Set key to new value if input has 2 chars
                            if len(self.cfg_ring_m) > 1:
                                # Convert from to list, edit value, convert back to tuple with integers
                                ring_config = list(self.ring)
                                ring_config[1] = self.cfg_ring_m
                                if int(ring_config[1]) > 26:
                                    ring_config[1] = 26
                                self.cfg_ring_m = str(ring_config[1])
                                self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                                # Reset machine with new ring value
                                reset_machine(self)
                                # Toggle the active variable.
                                self.cfg_ring_m_active = not self.cfg_ring_m_active
                                # Set input box color active / inactive
                                self.cfg_ring_m_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_m_active else CONFIG_INACTIVE_COLOR
                            else:
                                pass
                        elif event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            # Reset machine with new ring value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_ring_m_active = not self.cfg_ring_m_active
                            # Set input box color active / inactive
                            self.cfg_ring_m_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_m_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #  R I G H T   R O T O R   C O N F I G   #
                    elif self.cfg_rotor_r_active:
                        keyboard_input = event.unicode
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_r = right_rotor_type()
                        elif keyboard_input in "12345":
                            kb_long_clk_snd.play_sound()
                            self.cfg_rotor_r = keyboard_input
                            if keyboard_input == "1":
                                self.right_rotor = rotor_I
                            elif keyboard_input == "2":
                                self.right_rotor = rotor_II
                            elif keyboard_input == "3":
                                self.right_rotor = rotor_III
                            elif keyboard_input == "4":
                                self.right_rotor = rotor_IV
                            elif keyboard_input == "5":
                                self.right_rotor = rotor_V
                            # Reset machine with new key value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_rotor_r_active = not self.cfg_rotor_r_active
                            # Set input box color active / inactive
                            self.cfg_rotor_r_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_r_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #   R I G H T   R I N G   C O N F I G   #
                    elif self.cfg_ring_r_active:
                        keyboard_input = event.unicode
                        if keyboard_input in "1234567890":
                            kb_long_clk_snd.play_sound()
                            self.cfg_ring_r += keyboard_input
                            # Convert from to list, edit value, convert back to tuple with integers
                            ring_config = list(self.ring)
                            ring_config[2] = self.cfg_ring_r
                            self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                            # Set key to new value if input has 2 chars
                            if len(self.cfg_ring_r) > 1:
                                # Convert from to list, edit value, convert back to tuple with integers
                                ring_config = list(self.ring)
                                ring_config[2] = self.cfg_ring_r
                                if int(ring_config[2]) > 26:
                                    ring_config[2] = 26
                                self.cfg_ring_r = str(ring_config[2])
                                self.ring = tuple((int(ring_config[0]), int(ring_config[1]), int(ring_config[2])))
                                # Reset machine with new ring value
                                reset_machine(self)
                                # Toggle the active variable.
                                self.cfg_ring_r_active = not self.cfg_ring_r_active
                                # Set input box color active / inactive
                                self.cfg_ring_r_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_r_active else CONFIG_INACTIVE_COLOR
                            else:
                                pass
                        elif event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            # Reset machine with new ring value
                            reset_machine(self)
                            # Toggle the active variable.
                            self.cfg_ring_r_active = not self.cfg_ring_r_active
                            # Set input box color active / inactive
                            self.cfg_ring_r_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_r_active else CONFIG_INACTIVE_COLOR
                        else:
                            pass

                    #   P L U G B O A R D   C O N F I G   #
                    elif cfg_plugboard_active:
                        keyboard_input = event.unicode
                        # Reset Enigma with new plugboard config when ENTER is pressed
                        if event.key == pygame.K_RETURN:
                            kb_long_clk_snd.play_sound()
                            # Reset machine with new plugboard config
                            self.plugboard = Plug_board(cfg_plugboard)
                            reset_machine(self)
                            # Toggle the active variable.
                            cfg_plugboard_active = not cfg_plugboard_active
                            # Set input box color active / inactive
                            cfg_plugboard_border_color = CONFIG_ACTIVE_COLOR if cfg_plugboard_active else CONFIG_INACTIVE_COLOR
                        # Delete last char
                        elif event.key == pygame.K_BACKSPACE:
                            kb_long_clk_snd.play_sound()
                            cfg_plugboard = cfg_plugboard[:-1]
                        # Exit when Escape key is pressed
                        elif event.key == pygame.K_ESCAPE:
                            kb_long_clk_snd.play_sound()
                            # Reset machine with new plugboard config
                            self.plugboard = Plug_board(cfg_plugboard)
                            reset_machine(self)
                            # Toggle the active variable.
                            cfg_plugboard_active = not cfg_plugboard_active
                            # Set input box color active / inactive
                            cfg_plugboard_border_color = CONFIG_ACTIVE_COLOR if cfg_plugboard_active else CONFIG_INACTIVE_COLOR
                        else:
                            # Maximum of 10 plugboard cables
                            if len(used_letters) >= 20:
                                # Reset machine with new plugboard config
                                self.plugboard = Plug_board(cfg_plugboard)
                                reset_machine(self)
                                # Toggle the active variable.
                                cfg_plugboard_active = not cfg_plugboard_active
                                # Set input box color active / inactive
                                cfg_plugboard_border_color = CONFIG_ACTIVE_COLOR if cfg_plugboard_active else CONFIG_INACTIVE_COLOR
                            elif keyboard_input in "abcdefghijklmnopqrstuvwxyz":
                                kb_long_clk_snd.play_sound()
                                if keyboard_input.upper() in used_letters.upper():
                                    self.message = (f"You already used the letter {keyboard_input.upper()}. Choose another letter.")
                                else:
                                    used_letters += keyboard_input.upper()
                                    letter_combination += keyboard_input.upper()
                                    # Make a combination when 2 letters are entered
                                    if len(letter_combination) > 1:
                                        new_plugboard_config.append(letter_combination)
                                        # Cut one character from string if length of cfg_plugboard is odd
                                        cfg_plugboard = new_plugboard_config
                                        # Set plugboard to new config
                                        self.plugboard = Plug_board(cfg_plugboard)
                                        reset_machine(self)
                                        letter_combination = ""
                                    else:
                                        pass

                    # Exit when Escape key is pressed
                    elif event.key == pygame.K_ESCAPE:
                        self.message = ""
                        run = False

                    # Ignore keypresses from ignore list
                    elif event.key in ignore_list:
                        # Only play a sound
                        kb_long_clk_snd.play_sound()
                        self.message = ""

                    # Place a space when spacebar is pressed (no EN-DECODING)
                    elif event.key == pygame.K_SPACE:
                        kb_medium_clk_snd.play_sound()
                        self.INPUT = self.INPUT + " "
                        self.OUTPUT = self.OUTPUT + " "

                    # Shift output one line downwards when Enter is pressed and reset machine signal path
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        kb_long_clk_snd.play_sound()
                        line_feed(self)

                        # Reset machine after Enter Key
                        reset_machine(self)
                    else:
                        key = event.unicode

                        # Check if pressed key is in alphabet
                        if key in "abcdefghijklmnopqrstuvwxyz":
                            kb_short_clk_snd.play_sound()
                            letter = key.upper()
                            self.INPUT = self.INPUT + letter

                            # Enigma Encryption
                            self.PATH, cipher = self.ENIGMA.encipher(letter)
                            self.OUTPUT = self.OUTPUT + cipher

                            # Shift output when maximum number of characters exceed and reset machine
                            if len(self.INPUT) > max_chars-1:
                                line_feed(self)
                                self.INPUT = ""
                                self.OUTPUT = ""
                                self.PATH = []

                # Get mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Key input box selected
                    if self.cfg_key_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW KEY CONFIGURATION: Enter a new KEY combination of 3 letters"
                        # Toggle the active variable.
                        self.cfg_key_active = not self.cfg_key_active
                        # Clear Input
                        self.cfg_key = ""
                    # Key input box deselected
                    else:
                        self.cfg_key_active = False
                        self.cfg_key = self.key
                        reset_machine(self)

                    # Reflector input box selected
                    if self.cfg_reflector_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW REFLECTOR CONFIGURATION: Choose a reflector A, B or C"
                        # Toggle the active variable.
                        self.cfg_reflector_active = not self.cfg_reflector_active
                        # Clear Input
                        self.cfg_reflector = ""
                    # Reflector input box deselected
                    else:
                        self.cfg_reflector_active = False
                        self.cfg_reflector = reflector_type()
                        reset_machine(self)

                    # Left Rotor input box selected
                    if self.cfg_rotor_l_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW LEFT ROTOR CONFIGURATION: Choose 1 of the 5 rotors as left rotor"
                        # Toggle the active variable.
                        self.cfg_rotor_l_active = not self.cfg_rotor_l_active
                        # Clear Input
                        self.cfg_rotor_l = ""
                    # Left Rotor input box deselected
                    else:
                        self.cfg_rotor_l_active = False
                        self.cfg_rotor_l = left_rotor_type()
                        reset_machine(self)

                    # Left Ring input box selected
                    if self.cfg_ring_l_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW LEFT RING CONFIGURATION: Choose new ring value (0 - 26)"
                        # Toggle the active variable.
                        self.cfg_ring_l_active = not self.cfg_ring_l_active
                        # Clear Input
                        self.cfg_ring_l = ""

                    # Left Ring input box deselected
                    else:
                        self.cfg_ring_l_active = False
                        # Set value in inputbox
                        ring_value_l = list(self.ring)
                        if int(ring_value_l[0]) > 26:
                            ring_value_l[0] = 26
                        self.cfg_ring_l = str(ring_value_l[0])
                        reset_machine(self)

                    # Middle Rotor input box selected
                    if self.cfg_rotor_m_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW MIDDLE ROTOR CONFIGURATION: Choose 1 of the 5 rotors as middle rotor"
                        # Toggle the active variable.
                        self.cfg_rotor_m_active = not self.cfg_rotor_m_active
                        # Clear Input
                        self.cfg_rotor_m = ""
                    # Middle Rotor input box deselected
                    else:
                        self.cfg_rotor_m_active = False
                        self.cfg_rotor_m = middle_rotor_type()
                        reset_machine(self)

                    # Middle Ring input box selected
                    if self.cfg_ring_m_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW MIDDLE RING CONFIGURATION: Choose new ring value (0 - 26)"
                        # Toggle the active variable
                        self.cfg_ring_m_active = not self.cfg_ring_m_active
                        # Clear Input
                        self.cfg_ring_m = ""
                    # Middle Ring input box deselected
                    else:
                        # Toggle the active to inactive
                        self.cfg_ring_m_active = False
                        # Set value in inputbox
                        ring_value_m = list(self.ring)
                        if int(ring_value_m[1]) > 26:
                            ring_value_m[1] = 26
                        self.cfg_ring_m = str(ring_value_m[1])
                        reset_machine(self)

                    # Right Rotor input box selected
                    if self.cfg_rotor_r_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW RIGHT ROTOR CONFIGURATION: Choose 1 of the 5 rotors as right rotor"
                        # Toggle the active variable.
                        self.cfg_rotor_r_active = not self.cfg_rotor_r_active
                        # Clear Input
                        self.cfg_rotor_r = ""
                    # Right Rotor input box deselected
                    else:
                        self.cfg_rotor_r_active = False
                        self.cfg_rotor_r = right_rotor_type()
                        reset_machine(self)

                    # Right Ring input box selected
                    if self.cfg_ring_r_input_box.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW RIGHT RING CONFIGURATION: Choose new ring value (0 - 26)"
                        # Toggle the active variable.
                        self.cfg_ring_r_active = not self.cfg_ring_r_active
                        # Clear Input
                        self.cfg_ring_r = ""
                    # Right Ring input box deselected
                    else:
                        self.cfg_ring_r_active = False
                        # Set value in inputbox
                        ring_value_r = list(self.ring)
                        if int(ring_value_r[2]) > 26:
                            ring_value_r[2] = 26
                        self.cfg_ring_r = str(ring_value_r[2])
                        # Reset machine with new ring value
                        reset_machine(self)

                    # Plugboard input box selected
                    if plugboard_config_rect.collidepoint(event.pos):
                        kb_short_clk_snd.play_sound()
                        self.message = "NEW PLUGBOARD CONFIGURATION: Use max. 10 letter combinations for the new plugboard configuration"
                        # Empty list of already used plugboard letters
                        used_letters = ""
                        # Toggle the active variable.
                        cfg_plugboard_active = not cfg_plugboard_active
                        # Clear Input
                        cfg_plugboard = ""
                        new_plugboard_config = []
                    # Plugboard input box deselected
                    else:
                        cfg_plugboard_active = False
                        # Set plugboard to new input
                        self.plugboard = Plug_board(cfg_plugboard)
                        # Reset machine with new plugboard value
                        reset_machine(self)

                    # Change the current color of the input boxes.
                    self.cfg_key_border_color = CONFIG_ACTIVE_COLOR if self.cfg_key_active else CONFIG_INACTIVE_COLOR
                    self.cfg_reflector_border_color = CONFIG_ACTIVE_COLOR if self.cfg_reflector_active else CONFIG_INACTIVE_COLOR
                    self.cfg_rotor_l_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_l_active else CONFIG_INACTIVE_COLOR
                    self.cfg_ring_l_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_l_active else CONFIG_INACTIVE_COLOR
                    self.cfg_rotor_m_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_m_active else CONFIG_INACTIVE_COLOR
                    self.cfg_ring_m_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_m_active else CONFIG_INACTIVE_COLOR
                    self.cfg_rotor_r_border_color = CONFIG_ACTIVE_COLOR if self.cfg_rotor_r_active else CONFIG_INACTIVE_COLOR
                    self.cfg_ring_r_border_color = CONFIG_ACTIVE_COLOR if self.cfg_ring_r_active else CONFIG_INACTIVE_COLOR
                    cfg_plugboard_border_color = CONFIG_ACTIVE_COLOR if cfg_plugboard_active else CONFIG_INACTIVE_COLOR

            # Render machine
            draw_machine(self)

            # Update sceen
            pygame.display.flip()

        # Quit Game
        pygame.display.quit()
