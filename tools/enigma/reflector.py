# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/reflector.py
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
from config import EXTRA_LIGHT_PURPLE as REFLECTOR_BORDER_COLOR
from config import MEDIUM_GREEN as REFLECTOR_TXT_COLOR


class Reflector:

    def __init__(self, wiring):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = wiring

    # Reflect the signal through the reflector wiring
    def reflect(self, signal):
        # Find the letter at the signal[index] place
        letter = self.right[signal]
        # Convert letter to new signal after wiring
        signal = self.left.find(letter)
        return signal

    # Draw rotor
    def draw(self, screen, x_pos, y_pos, width, height, font):

        # Rectangle
        r = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(screen, REFLECTOR_BORDER_COLOR, r, width=1, border_radius=15)

        # Letters
        for i in range(26):
            # Draw left side of reflector
            letter = self.left[i]
            letter = font.render(letter, True, REFLECTOR_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width/4, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)

            # Draw right side of reflector
            letter = self.right[i]
            letter = font.render(letter, True, REFLECTOR_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width*3/4, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)
