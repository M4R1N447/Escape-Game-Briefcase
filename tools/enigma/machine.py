# __________________________________________________
# FILE: game/Briefcase Pi 3B/Enigma/enigma.py
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

# Config color Settings
from config import LIGHT_GREEN as COMPONENT_NAME_COLOR
from config import EXTRA_LIGHT_GREEN as SIGNAL_FORWARD_COLOR
from config import RED as SIGNAL_BACKWARD_COLOR
from config import YELLOW as SIGNAL_REFLECTOR_COLOR


class Enigma:

    def __init__(self, reflector, rotor_I, rotor_II, rotor_III, plugboard, keyboard):
        self.reflector = reflector
        self.rotor_I = rotor_I
        self.rotor_II = rotor_II
        self.rotor_III = rotor_III
        self.plugboard = plugboard
        self.keyboard = keyboard

    def set_ring(self, ring):
        self.rotor_I.set_ring(ring[0])
        self.rotor_II.set_ring(ring[1])
        self.rotor_III.set_ring(ring[2])

    # Set the 3 digit encryption key of the Enigma
    def set_key(self, key):
        # Rotate rotor I to first letter of the key
        self.rotor_I.rotate_to_letter(key[0])
        # Rotate rotor II to second letter of the key
        self.rotor_II.rotate_to_letter(key[1])
        # Rotate rotor III to third letter of the key
        self.rotor_III.rotate_to_letter(key[2])

    # Encipher a letter
    def encipher(self, letter):

        # Rotate the rotors
        # All Rotors will only turn when notches of rotor II and III are aligned
        if self.rotor_II.left[0] == self.rotor_II.notch and self.rotor_III.left[0] == self.rotor_III.notch:
            self.rotor_I.rotate()
            self.rotor_II.rotate()
            self.rotor_III.rotate()
        # Also when middle rotors notch aligned all rotors turn
        # This is same as original enigma machine as extra cipher
        # Called double step anomaly
        elif self.rotor_II.left[0] == self.rotor_II.notch:
            self.rotor_I.rotate()
            self.rotor_II.rotate()
            self.rotor_III.rotate()
        # Rotor II and III will turn when notch of rotor III is aligned
        elif self.rotor_III.left[0] == self.rotor_III.notch:
            self.rotor_II.rotate()
            self.rotor_III.rotate()
        else:
            self.rotor_III.rotate()

        # Pass signal through the machine
        signal = self.keyboard.forward(letter)
        path = [signal, signal]
        signal = self.plugboard.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_III.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_II.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_I.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.reflector.reflect(signal)
        path.append(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_I.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_II.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.rotor_III.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.plugboard.forward(signal)
        path.append(signal)
        path.append(signal)
        letter = self.keyboard.backward(signal)
        return path, letter

    def draw(self, path, screen, width, height, margins, gap, font):

        # Width and Height of Enigma Components
        component_width = (width - margins["left"] - margins["right"] - 5 * gap)/6
        component_height = height - margins["top"] - margins["bottom"]

        # Path Coordinates
        # Get X and Y coordinates of the letters in the path
        y_coord = [margins["top"] + (signal + 1) * (component_height / 27) for signal in path]

        # Keyboard
        x_coord = [width - margins["right"] - (component_width / 2)]

        # Forward pass
        for i in [4, 3, 2, 1, 0]:
            x_coord.append(margins["left"] + i * (component_width + gap) + (component_width * 3/4))
            x_coord.append(margins["left"] + i * (component_width + gap) + (component_width * 1/4))

        # Reflector
        x_coord.append(margins["left"] + (component_width * 3/4))

        # backward pass
        for i in [1, 2, 3, 4]:
            x_coord.append(margins["left"] + i * (component_width + gap) + (component_width * 1/4))
            x_coord.append(margins["left"] + i * (component_width + gap) + (component_width * 3/4))

        # Lamp Board
        x_coord.append(width - margins["right"] - (component_width / 2))

        # Draw path
        if len(path) > 0:
            for i in range(1, 21):
                # Forward Color
                if i < 10:
                    color = SIGNAL_FORWARD_COLOR
                # Reflector Color
                elif i < 12:
                    color = SIGNAL_REFLECTOR_COLOR
                # Backward Color
                else:
                    color = SIGNAL_BACKWARD_COLOR

                start = (x_coord[i-1], y_coord[i-1])
                end = (x_coord[i], y_coord[i])

                pygame.draw.line(screen, color, start, end, width=3)

        # Base coordinates
        x_pos = margins["left"]
        y_pos = margins["top"]

        # Draw Enigma Components
        for component in [self.reflector,
                          self.rotor_I,
                          self.rotor_II,
                          self.rotor_III,
                          self.plugboard,
                          self.keyboard]:
            component.draw(screen, x_pos, y_pos, component_width, component_height, font)
            x_pos += component_width + gap

        # Component Names
        names = ["Reflector", "Left", "Middle", "Right", "Plugboard", "Key/Lamp"]
        y = margins["top"] * 0.95

        for i in range(6):
            x = margins["left"] + component_width/2 + i * (component_width + gap)
            title = font.render(names[i], True, COMPONENT_NAME_COLOR)
            text_box = title.get_rect(center=(x, y))
            screen.blit(title, text_box)
