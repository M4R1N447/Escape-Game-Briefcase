# ___________________________________________________________________
#  ____     ____  __  .'`",.'`",.- WWW.MARIOKUIJPERS.COM -.'`",.'`",.
#  |   \   /   | / /            .-.    .-.    ,.--.
#  | |\ \ / /| |/ /  2024      | OO|  | OO|  /  _.-' .-. .-. .-. .''.
#  | | \   / |    \  MARIO     |   |  |   |  \   '-. '-' '-' '-' '..'
#  |_|  \_/  |_| \_\ KUIJPERS  '^^^'  '^^^'   `'--'
# ___________________________________________________________________
#
# FILE: config.py
# INFO: Config File for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 06-01-2021
# Last update: 06-07-2024
# Github: https://github.com/M4R1N447/EscapeGame
# Status: In Progress
# ___________________________________________________________________

# IMPORTS
import platform
import creds

#
#      D E B U G   M O D E   O N   /   O F F       #
# __________________________________________________

DEBUG_MODE = True
BIG_SCREEN = False

#
#           A U D I O   O N   /   O F F            #
# __________________________________________________

AUDIO = True
MUSIC = True
SPEECH = True

#
#   U S E R   L O G I N   &   P A S S W O R D S    #
# __________________________________________________

if DEBUG_MODE:
    PASSWORD = ""
    ADMIN_PASSWORD = "admin"
else:
    PASSWORD = creds.PASSWORD
    ADMIN_PASSWORD = creds.ADMIN_PASSWORD

#
#               S M T P   G m a i l                #
# __________________________________________________

SMTP_SERVER = creds.smtp_server
SMTP_PORT = creds.smtp_port
SMTP_USERNAME = creds.smtp_username
SMTP_PASSWORD = creds.smtp_password

#
#                    P A T H S                     #
# __________________________________________________

# Set driveletter for Windows Machines
drive = "P:/"

# WINDOWS SPECIFIC
if platform.system() == "Windows":
    OS_PLATFORM = "Windows"
    PRE = drive
    CHROME_DRIVER_PATH = PRE + "game/Briefcase Pi 3B/chromedriver/windows/chromedriver.exe"

# LINUX SPECIFIC
else:
    OS_PLATFORM = "Linux"
    PRE = "/home/pi/"
    CHROME_DRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"

# PATHS
GAME_PATH = PRE + "game/Briefcase Pi 3B/"
IMAGE_PATH = PRE + "game/Briefcase Pi 3B/images/"
FONT_PATH = PRE + "game/Briefcase Pi 3B/fonts/"
DB_PATH = PRE + "game/Briefcase Pi 3B/"
SOUNDTRACK_PATH = PRE + "game/Briefcase Pi 3B/audio/soundtrack/"
SOUND_PATH = PRE + "game/Briefcase Pi 3B/audio/sounds/"
VIDEO_PATH = PRE + "game/Briefcase Pi 3B/video/"
QR_PATH = PRE + "game/Briefcase Pi 3B/qrcode/"
MAP_PATH = PRE + "game/Briefcase Pi 3B/"
MEMORY_IMAGES_PATH = PRE + "game/Briefcase Pi 3B/Memory/images/"
SPACE_INVADERS_PATH = PRE + "game/Briefcase Pi 3B/space_invaders/"
PACMAN_PLAYER_IMG_PATH = PRE + "game/Briefcase Pi 3B/Pacman/images/player_images/"
PACMAN_GHOST_IMG_PATH = PRE + "game/Briefcase Pi 3B/Pacman/images/ghost_images/"
PACMAN_SOUNDS_PATH = PRE + "game/Briefcase Pi 3B/Pacman/sounds/"

#
#                 T I M E Z O N E                  #
# __________________________________________________

TIMEZONE = "Europe/Amsterdam"

#
#               S C R E E N S I Z E                #
# __________________________________________________

GEOMETRY = "1024x768"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

#
#            L I N K S   &   U R L ' s             #
# __________________________________________________

# Browser URL's
MARIO_URL = "https://mariokuijpers.com"
MAPS_URL = (MAP_PATH + "map.html")

#
#                    F O N T S                     #
#
# Usable fonts: "Share Tech Regular", "MrRobot",
# "Elite Hacker (Corroded)", "Arcade", "Orbitron-Black.ttf",
# "Cyberdyne.ttf"
# __________________________________________________

# Used fonts which are loaded by PyQt5
FONT1 = "MrRobot"
FONT2 = "Share Tech Regular"
FONT3 = "Arcade"

# Header Font (MrRobot)
HEADER_FONT = FONT1 
if BIG_SCREEN:
    HEADER_FONT_SIZE = 80
else:
    HEADER_FONT_SIZE = 80

# Title Font
TITLE_FONT = FONT1  # "MrRobot"
if BIG_SCREEN:
    TITLE_FONT_SIZE = 60
else:
    TITLE_FONT_SIZE = 60

# Subtitle Font
SUBTITLE_FONT = FONT3  # "Share Tech Regular"
if BIG_SCREEN:
    SUBTITLE_FONT_SIZE = 20
else:
    SUBTITLE_FONT_SIZE = 20

# Main Font
MAIN_FONT = FONT2  # "Share Tech Regular"
if BIG_SCREEN:
    MAIN_FONT_SIZE = 14
else:
    MAIN_FONT_SIZE = 14
MAIN_FONT_SIZE_BIG = 18

# Button Font
BUTTON_FONT = FONT3  # "Arcade"
if BIG_SCREEN:
    BUTTON_FONT_SIZE = 20
else:
    BUTTON_FONT_SIZE = 20

# Button Font
MENU_BUTTON_FONT = FONT3  # "Arcade"
if BIG_SCREEN:
    MENU_BUTTON_FONT_SIZE = 20
else:
    MENU_BUTTON_FONT_SIZE = 20

# Standard Font
STANDARD_FONT = FONT2  # "Share Tech Regular"
if BIG_SCREEN:
    STANDARD_FONT_SIZE = 14
else:
    STANDARD_FONT_SIZE = 14

# Bottom Font
BOTTOM_FONT = FONT2  # "Share Tech Regular"
BOTTOM_FONT_SIZE = 10

# Splash Screen Font
SPLASH_FONT = FONT3  # "Arcade"
if BIG_SCREEN:
    SPLASH_FONT_SIZE_HUGE = 60
    SPLASH_FONT_SIZE_BIG = 40
else:
    SPLASH_FONT_SIZE_HUGE = 40
    SPLASH_FONT_SIZE_BIG = 20

#
#                   C O L O R S                    #
#
# https://colorpicker.me/#000000
# __________________________________________________

# Predefined RGB Colors
WHITE = (255, 255, 255)  # #ffffff
LIGHT_GRAY = (222, 222, 222)  # #dedede
GRAY = (128, 128, 128)  # #808080 (50% GREY)
EXTRA_DARK_GRAY = (10, 10, 15)  # #0a0a0f
BLACK = (0, 0, 0)  # #000000

EXTRA_LIGHT_RED = (230, 187, 173)  # #e6bbad (Complementary LIGHT_BLUE)
LIGHT_RED = (236, 94, 94)  # #ec5e5e
RED = (255, 0, 0)  # #ff0000 (Complementary LIGHT_BLUE)
MEDIUM_RED = (205, 32, 32)  # #cd2020
DARK_RED = (154, 36, 36)  # #9a2424
EXTRA_DARK_RED = (111, 36, 36)  # #6f2424

EXTRA_LIGHT_BLUE = (173, 216, 230)  # #add8e6  (Complementary LIGHT_ORANGE)
LIGHT_BLUE = (0, 255, 255)  # #00ffff (Complementary RED)
MEDIUM_BLUE = (0, 127, 255)  # #007fff (Complementary ORANGE)
BLUE = (0, 0, 255)  # #0000ff (Complementary YELLOW)
DARK_BLUE = (50, 50, 150)  # #323296
EXTRA_DARK_BLUE = (45, 45, 104)  # #2d2d68

EXTRA_LIGHT_GREEN = (153, 255, 153)  # #99ff99 (Complementary EXTRA_LIGHT_PINK)
LIGHT_GREEN = (0, 230, 0)  # #00e600 (Complementary LIGHT_PINK)
GREEN = (0, 255, 0)  # #00ff00
MEDIUM_GREEN = (0, 188, 80)  # #00bc50 (Complementary PINK)
DARK_GREEN = (29, 133, 73)  # #1d8549
EXTRA_DARK_GREEN = (45, 68, 49)  # #2d4431 (Complementary PURPLE)

EXTRA_LIGHT_YELLOW = (250, 250, 182)  # #fafab6
LIGHT_YELLOW = (249, 249, 135)  # #f9f987
YELLOW = (255, 255, 0)  # #ffff00 (Complementary BLUE)
MEDIUM_YELLOW = (213, 213, 53)  # #d5d535
DARK_YELLOW = (161, 161, 63)  # #a1a13f
EXTRA_DARK_YELLOW = (92, 92, 61)  # #5c5c3d (Complementary LIGHT_PURPLE)

EXTRA_LIGHT_ORANGE = (251, 182, 113)  # #fbb671
LIGHT_ORANGE = (255, 179, 0)  # #ffb300
ORANGE = (255, 128, 0)  # #ff8000 (Complementary MEDIUM_BLUE)
MEDIUM_ORANGE = (220, 122, 22)  # #dc7a16
DARK_ORANGE = (255, 77, 0)  # #ff4d00
EXTRA_DARK_ORANGE = (166, 70, 29)  # #a6461d

EXTRA_LIGHT_PINK = (255, 153, 255)  # #ff99ff (Complementary EXTRA_LIGHT_GREEN)
LIGHT_PINK = (230, 0, 230)  # #e600e6 (Complementary LIGHT_GREEN)
PINK = (255, 0, 255)  # #ff00ff
MEDIUM_PINK = (188, 0, 108)  # #bc006c (Complementary GREEN)
DARK_PINK = (128, 77, 128)  # #804d80
EXTRA_DARK_PINK = (110, 29, 110)  # #6e1d6e)

EXTRA_LIGHT_PURPLE = (161, 121, 234)  # #a179ea
LIGHT_PURPLE = (61, 61, 92)  # #3d3d5c (Complementary EXTRA_DARK_YELLOW)
PURPLE = (153, 0, 255)  # #9900ff
MEDIUM_PURPLE = (44, 33, 64)  # #2c2140 (Complementary DARK_GREEM)
DARK_PURPLE = (31, 31, 46)  # #1f1f2e
EXTRA_DARK_PURPLE = (10, 10, 15)  # #0a0a0f

# Background Colors
BG_COLOR = DARK_PURPLE
BG_LIGHT_COLOR = LIGHT_PURPLE
BG_DARK_COLOR = EXTRA_DARK_PURPLE
BG_STATUSBAR_COLOR = LIGHT_GRAY

# Main Font Colors
MAIN_FONT_COLOR = LIGHT_GREEN
MAIN_DARK_FONT_COLOR = GREEN
MAIN_LIGHT_FONT_COLOR = EXTRA_LIGHT_GREEN

# Button Colors
BTN_MOUSE_OVER_COLOR = LIGHT_GREEN
BTN_MOUSE_OUT_COLOR = LIGHT_PURPLE
BTN_MOUSE_CLICKED_COLOR = EXTRA_LIGHT_GREEN

# Inputbox Colors
INPUT_BG_COLOR = WHITE
INPUT_FONT_COLOR = BLACK

# Header Font Color
HEADER_FONT_COLOR = LIGHT_GREEN

# Title Font Color
TITLE_FONT_COLOR = LIGHT_GREEN

# Subtitle
SUBTITLE_FONT_COLOR = LIGHT_GREEN

# Standard Text Font
STANDARD_FONT_COLOR = LIGHT_GREEN

# Splashscreen
SPLASH_FONT_COLOR = LIGHT_GREEN

# QR Code Generator
QR_FILL_COLOR = BLACK
QR_BG_COLOR = WHITE

# Briefcase background and border colors
BRIEFCASE_BORDER_COLOR = WHITE
BRIEFCASE_BG_COLOR = DARK_PURPLE
BRIEFCASE_MAIN_BG_COLOR = PURPLE

# Briefcase LED Matrix Colors
BRIEFCASE_MATRIX_BG_COLOR = EXTRA_DARK_GRAY

# Briefcase LED Colors
BRIEFCASE_STD_LED_ON_COLOR = GREEN
BRIEFCASE_STD_LED_OFF_COLOR = BLACK
BRIEFCASE_LED_BG_COLOR = BLUE

# Briefcase LCD Colors
LCD_BG_COLOR = BLUE

# Briefcase Meter Colors
METER_COLOR = YELLOW

# Briefcase Tuimelschakelaar Colors
SWITCH_BG_COLOR = BLUE
SWITCH_COLOR = YELLOW

# Briefcase Keypad Colors
KEY_COLOR = YELLOW

#
#           I M A G E S   &   I C O N S            #
# __________________________________________________

# Icons
SERVER_ICON = (IMAGE_PATH + "server.png")
LOCK_ICON = (IMAGE_PATH + "lock.png")
ENCRYPTION_ICON = (IMAGE_PATH + "encryption.png")
HACKER_ICON = (IMAGE_PATH + "hacker.png")

# Images
if BIG_SCREEN:
    MR_ROBOT_IMG = (IMAGE_PATH + "mrrobot.png")
    MEMORY_BG = (MEMORY_IMAGES_PATH + "memory_bg.jpg")
    # mrrobot.jpg
else:
    MR_ROBOT_IMG = (IMAGE_PATH + "mrrobot_small.jpg")
    MEMORY_BG = (MEMORY_IMAGES_PATH + "memory_bg.jpg")

ACCES_DENIED = (IMAGE_PATH + "acces_denied.png")

#
#            A U D I O   &   S O U N D             #
# __________________________________________________

# STARTSCREEN
STARTSCREEN_BG_AUDIO = (SOUNDTRACK_PATH + "one2blame_orc.mp3")

# MENU
MENU_BG_AUDIO = (SOUNDTRACK_PATH + "fucksociety_mp3.mp3")

# LOGIN_TRACK = (SOUNDTRACK_PATH + "undo_gpx")
# MAIN_MENU_TRACK = (SOUNDTRACK_PATH + "kill-process_rip")
# TOOLS_MENU_TRACK = (SOUNDTRACK_PATH + "contractor")

# MEMORY GAME
MEMORY_BG_AUDIO = (SOUNDTRACK_PATH + "hackthepolice_mp3.mp3")
MEMORY_CLICK_SND = (SOUND_PATH + "keyboard_short_click.mp3")

# PACMAN
PACMAN_BG_AUDIO = (SOUNDTRACK_PATH + "kill-process_rip.mp3")

# ENIGMA TOOL
ENIGMA_BG_AUDIO = (SOUNDTRACK_PATH + "askingthe1mpossible_m4p.mp3")
ENIGMA_SHORT_CLK_SND = (SOUND_PATH + "keyboard_short_click.mp3")
ENIGMA_MEDIUM_CLK_SND = (SOUND_PATH + "keyboard_medium_click.mp3")
ENIGMA_LONG_CLK_SND = (SOUND_PATH + "keyboard_long_click.mp3")

# PERIODIC TABLE TOOL
PERIODIC_TABLE_BG_AUDIO = (SOUNDTRACK_PATH + "askingthe1mpossible_m4p.mp3")

# VIDEO
testvideo1 = VIDEO_PATH + "2.mp4"

#
#          C S S   S T Y L E S H E E T S           #
# __________________________________________________

WINDOW_CSS = ("background-color: rgb" + str(BG_COLOR) + ";")

# Header label Red stylesheet
HEADER_LBL_CSS = (
        "color: rgb" + str(RED) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 0px 2px 0px;"
        "aligntop;"
    )

# Title label stylesheet
TITLE_LBL_CSS = (
        "color: rgb" + str(TITLE_FONT_COLOR) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 0px 2px 0px;"
    )

# Subtitle label stylesheet
SUBTITLE_LBL_CSS = (
        "color: rgb" + str(SUBTITLE_FONT_COLOR) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 0px 2px 0px;"
    )

# Splash label stylesheet
SPLASH_LBL_CSS = (
        "color: rgb" + str(SPLASH_FONT_COLOR) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 0px 2px 0px;"
    )

# Warning text label stylesheet
WARNING_LBL_CSS = (
        "color: rgb" + str(RED) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 2px 2px 2px;"
    )

# Text label stylesheet
TEXT_LBL_CSS = (
        "color: rgb" + str(MAIN_DARK_FONT_COLOR) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 2px 2px 2px;"
    )

# Storyline label stylesheet
STORYLINE_LBL_CSS = (
    "color: rgb" + str(LIGHT_BLUE) + ";" +
    "background-color: rgb" + str(BG_COLOR) + ";" +
    "padding: 0px 0px;" +
    "margin: 2px 0px 2px 0px;"
    "text-align:left;"
)

# Puzzle label stylesheet
PUZZLE_LBL_CSS = (
        "color: rgb" + str(RED) + ";" +
        "background-color: rgb" + str(BG_COLOR) + ";" +
        "padding: 0px 0px;" +
        "margin: 2px 0px 2px 0px;"
    )

# Logo image stylesheet
LOGO_CSS = (
    "margin-top: 30px;"
    "margin-bottom: 20px;"
    )

# Button stylesheet
BTN_CSS = (
    "*{color: rgb" + str(BTN_MOUSE_OVER_COLOR) + ";" +
    # top, bottom, left, right
    "padding: 25px, 20px;" +
    "margin: 5px 5px 5px 5px;" +
    "border: 2px solid rgb" + str(BTN_MOUSE_OVER_COLOR) + ";" +
    "border-radius: 20px;}" +
    "*:hover{background: rgb" + str(BTN_MOUSE_OVER_COLOR) + ";" +
    "color: rgb" + str(BTN_MOUSE_OUT_COLOR) + ";}"
    )

# Text input stylesheet
TXT_INPUT_CSS = (
    "*{color: rgb" + str(BTN_MOUSE_OVER_COLOR) + ";" +
    # top, bottom, left, right
    "padding: 25px, 20px;" +
    "margin: 5px 5px 5px 5px;" +
    "border: 2px solid rgb" + str(BTN_MOUSE_OVER_COLOR) + ";" +
    "border-radius: 5px;}"
    )

#
# P U Z Z L E ,   M E D I A  &  T O O L   D A T A  #
# __________________________________________________

# PATHS to append to system Path
PUZZLE_PATHS = [GAME_PATH + "Crack_the_code/",
                GAME_PATH + "Memory/",
                GAME_PATH + "Pacman/",
                GAME_PATH + "Enigma/",
                GAME_PATH + "Periodic_Table/"
                ]

#
#               L E V E L   D A T A                #
# __________________________________________________

''' L E V E L   1 '''

STORYLINE_LIST = [
    {"level": 1, "story": "An anonymous hacker group reported some strange activities going on...\n\n"\
    "We need someone to find out what it is. Do you have what it takes to help us?\n"\
    "Are you the one we need? Show us your skills!\n\n"\
    "You first need to find more information on those hackers.\n"\
    "Can we trust their info? Who are they? From where do they operate?\n\n"\
    "You will need to find answers and info thru puzzles, games and media.\n"\
    "This game consists of multiple phases, levels, games and puzzles. Have Fun!\n\n"},
    {"level": 2, "story": "Boejuh"},
    {"level": 3, "story": "3 x Boejuh"}
    ]

# Solution to complete level 1
LEVEL1_SOLUTION = "ABCD"

# Level 1 Puzzle Data [name, max score to earn, input data]
PUZZLES1 = [
    {"name": "game_info", "score": 0, "input": LEVEL1_SOLUTION, "complexity": None, "sound": MEMORY_BG_AUDIO, "volume": 0.2},
    {"name": "crack_the_code", "score": 100, "input": None, "complexity": None, "sound": MEMORY_BG_AUDIO, "volume": 0.2},
    {"name": "crack_the_code2", "score": 200, "input": None, "complexity": None, "sound": MEMORY_BG_AUDIO, "volume": 0.2},
    {"name": "memory", "score": 300, "input": None, "complexity": "bin", "sound": MEMORY_BG_AUDIO, "volume": 0.2},
    {"name": "pacman", "score": 500, "input": LEVEL1_SOLUTION, "complexity": None, "sound": PACMAN_BG_AUDIO, "volume": 0.2}
    ]

# Tools that can be used in this level
TOOLS1 = [
    {"name": "enigma", "sound": ENIGMA_BG_AUDIO, "volume": 0.2},
    {"name": "periodic_table", "sound": PACMAN_BG_AUDIO, "volume": 0.2}
]

# Media that can be used in this level
MEDIA1 = [
    {"name": "media"},
    {"name": "media"}
    ]


''' L E V E L   2 '''

# Solution to complete level 2
LEVEL2_SOLUTION = "EFGH"

# Level 2 Puzzle Data [name, max score to earn, input data]
PUZZLES2 = [
    {"name": "game_info", "score": 0, "input": LEVEL2_SOLUTION},
    {"name": "crack_the_code2", "score": 200, "input": LEVEL2_SOLUTION},
    {"name": "memory", "score": 300, "input": LEVEL2_SOLUTION},
    {"name": "pacman", "score": 500, "input": LEVEL2_SOLUTION}
    ]

# Tools that can be used in this level
TOOLS2 = [
    {"name": "enigma", "score": 0, "input": None},
    {"name": "pacman", "score": 0, "input": None},
    {"name": "enigma", "score": 0, "input": None}
]

# Media that can be used in this level
MEDIA2 = [
    {"name": "?", "score": 0, "input": None},
    {"name": "?", "score": 0, "input": None}
    ]

''' L E V E L   3 '''

# Solution to complete level 3
LEVEL3_SOLUTION = "IJKL"

# Level 3 Puzzle Data [name, max score to earn, input data]
PUZZLES3 = [
    {"name": "game_info", "score": 0, "input": LEVEL3_SOLUTION},
    {"name": "crack_the_code", "score": 100, "input": LEVEL3_SOLUTION}
    ]

# Tools that can be used in this level
TOOLS3 = [
   {"name": "?", "score": 0, "input": None},
    {"name": "?", "score": 0, "input": None}
    ]

# Media that can be used in this level
MEDIA3 = [
    {"name": "?", "score": 0, "input": None},
    {"name": "?", "score": 0, "input": None}
    ]

# List of lists of puzzle dictonaries per level
LEVEL_LIST = [PUZZLES1, PUZZLES2, PUZZLES3]

# List of lists of tool dictonaries per level
TOOL_LIST = [TOOLS1, TOOLS2, TOOLS3]

# List of lists of media dictonaries per level
MEDIA_LIST = [MEDIA1, MEDIA2, MEDIA3]

# List of Solutions
SOLUTION_LIST = [LEVEL1_SOLUTION,
                 LEVEL2_SOLUTION,
                 LEVEL3_SOLUTION]


#
#            B R I E F C A S E   I / O             #
# __________________________________________________

# 10 Turn Potmeter Offsets
POT1_OFFSET = 0
POT2_OFFSET = 0
POT3_OFFSET = 0
POT4_OFFSET = 0
POT5_OFFSET = 0
POT6_OFFSET = 0
POT7_OFFSET = 0
POT8_OFFSET = 0
POT9_OFFSET = 0
POT10_OFFSET = 0
POT11_OFFSET = 0
POT12_OFFSET = 0
POT13_OFFSET = 0
POT14_OFFSET = 0
