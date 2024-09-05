# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/key_board.py
# INFO: Enigma Encoder / Decoder for Escape Game: Mr Robot
#
# Author: Mario Kuijpers
# Start date: 17-04-2023
# Last update: 18-04-2023
# Github: https://github.com/M4R1N447/Mr.-Robot-Escape-Game-Briefcase
# Status: In Progress
# __________________________________________________

# Imports
import pygame

# Config Color Settings
from config import EXTRA_LIGHT_PURPLE as KEYBOARD_BORDER_COLOR
from config import MEDIUM_GREEN as KEYBOARD_TXT_COLOR


class Key_board:

    # Convert letter to a signal
    def forward(self, letter):
        # Find letter and get index
        signal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        return signal

    # Convert signal to a letter
    def backward(self, signal):
        # Find index and get letter
        letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal]
        return letter

    # Draw the keyboard
    def draw(self, screen, x_pos, y_pos, width, height, font):

        # Rectangle
        r = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(screen, KEYBOARD_BORDER_COLOR, r, width=1, border_radius=15)

        # Letters
        for i in range(26):
            letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
            letter = font.render(letter, True, KEYBOARD_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width/2, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)
