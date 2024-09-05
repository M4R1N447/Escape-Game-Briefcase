# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/rotor.py
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
from config import EXTRA_LIGHT_PURPLE as ROTOR_BORDER_COLOR
from config import LIGHT_GREEN as ROTOR_NOTCH_COLOR
from config import EXTRA_LIGHT_PURPLE as ROTOR_HIGHLIGHT_COLOR
from config import YELLOW as ROTOR_HIGHLIGHT_TXT_COLOR
from config import EXTRA_DARK_PURPLE as ROTOR_NOTCH_TXT_COLOR
from config import MEDIUM_GREEN as ROTOR_TXT_COLOR


class Rotor:

    def __init__(self, wiring, notch):
        # Left side of rotor is alphabet
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Right side of rotor is wired/coded alphabet
        self.right = wiring
        # Notch place on rotor
        self.notch = notch

    # Convert the letter through the rotor wiring in forward signal
    def forward(self, signal):
        # Find the letter at the signal[index] place (right side of rotor)
        letter = self.right[signal]
        # Convert letter to new signal after wiring (left side of rotor)
        signal = self.left.find(letter)
        return signal

    # Convert the letter through the rotor wiring in backward signal
    def backward(self, signal):
        # Find the letter at the signal[index] place (left side of rotor)
        letter = self.left[signal]
        # Convert letter to new signal after wiring (right side of rotor)
        signal = self.right.find(letter)
        return signal

    # Show the rotor
    def show(self):
        # Print left side of the rotor
        print(self.left)
        # Print right side of the rotor
        print(self.right)
        print("")

    # Rotate the rotor n steps
    def rotate(self, n=1, forward=True):
        for _ in range(n):
            if forward:
                # Rotate forward
                self.left = self.left[1:] + self.left[0]
                self.right = self.right[1:] + self.right[0]
            else:
                # Rotate backward
                self.left = self.left[25] + self.left[:25]
                self.right = self.right[25] + self.right[:25]

    # Rotate to given letter
    def rotate_to_letter(self, letter):
        # Find index of letter
        n = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        self.rotate(n)

    def set_ring(self, n):

        # Rotate the rotor backwards
        # Set number of steps (n) to 0 and rotor backwards
        self.rotate(n-1, forward=False)

        # Adjust the turnover notch in relationship to the wiring
        # Find the index of the notch
        n_notch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(self.notch)
        # Set notch to new position using modulo function
        self.notch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[(n_notch - n) % 26]

    # Draw rotor
    def draw(self, screen, x_pos, y_pos, width, height, font):

        # Rectangle
        r = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(screen, ROTOR_BORDER_COLOR, r, width=1, border_radius=15)

        # Letters
        for i in range(26):
            # Draw left side of rotor
            letter = self.left[i]
            if i == 0:
                letter = font.render(letter, True, ROTOR_HIGHLIGHT_TXT_COLOR)
            else:
                letter = font.render(letter, True, ROTOR_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width/4, y_pos+(i+1)*height/27))

            # highlight top letter
            if i == 0:
                pygame.draw.rect(screen, ROTOR_HIGHLIGHT_COLOR, text_box, border_radius=5)

            # highlight turnover notch
            if self.left[i] == self.notch:
                letter = font.render(self.notch, True, ROTOR_NOTCH_TXT_COLOR)
                pygame.draw.rect(screen, ROTOR_NOTCH_COLOR, text_box, border_radius=5)
            screen.blit(letter, text_box)

            # Draw right side of rotor
            letter = self.right[i]
            letter = font.render(letter, True, ROTOR_TXT_COLOR)
            text_box = letter.get_rect(center=(x_pos+width*3/4, y_pos+(i+1)*height/27))
            screen.blit(letter, text_box)
