# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/plug_board.py
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
from config import EXTRA_LIGHT_PURPLE as PLUGBOARD_BORDER_COLOR
from config import MEDIUM_GREEN as PLUGBOARD_TXT_COLOR


class Plug_board:

    def __init__(self, pairs):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Swap letters for each given pair
        for pair in pairs:
            A = pair[0]
            B = pair[1]
            pos_A = self.left.find(A)
            pos_B = self.left.find(B)
            # Swap positions for A and B
            self.left = self.left[:pos_A] + B + self.left[pos_A+1:]
            self.left = self.left[:pos_B] + A + self.left[pos_B+1:]

    # Swap letters in forward signal
    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    # Swap letters in backward signal
    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

    # Draw the plugboard
    def draw(self, screen, x_pos, y_pos, width, height, font):

        # Rectangle
        r = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(screen, PLUGBOARD_BORDER_COLOR, r, width=1, border_radius=15)

        # Letters
        for i in range(26):
            # Draw left side of plugboard
            letter = self.left[i]
            letter = font.render(letter, True, PLUGBOARD_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width/4, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)

            # Draw right side of plugboard
            letter = self.right[i]
            letter = font.render(letter, True, PLUGBOARD_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width*3/4, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)
