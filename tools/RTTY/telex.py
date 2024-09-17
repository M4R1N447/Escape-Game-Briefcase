import time
import numpy as np
import pygame

# Baudot-coderingstabel
baudot_table = {
    ' ': '00000',
    'A': '00011',
    'B': '11010',
    'C': '01110',
    'D': '00111',
    'E': '00110',
    'F': '01011',
    'G': '11100',
    'H': '01101',
    'I': '10001',
    'J': '10110',
    'K': '11001',
    'L': '10101',
    'M': '11110',
    'N': '01111',
    'O': '10011',
    'P': '11011',
    'Q': '10111',
    'R': '01001',
    'S': '01010',
    'T': '00101',
    'U': '10100',
    'V': '10010',
    'W': '01100',
    'X': '11101',
    'Y': '10000',
    'Z': '01000',
    '\n': '00010'  # nieuwe regel
}

# Instellingen voor de tonen
freq_0 = 2125  # frequentie voor '0'
freq_1 = 2295  # frequentie voor '1'
baud_rate = 45.45  # baud rate van RTTY-signaal
sample_rate = 44100  # aantal samples per seconde
duration = 0.1  # duur van elke toon in seconden

# Bereken het aantal samples per toon
samples_per_tone = int(sample_rate / baud_rate)
t = np.arange(0, duration, 1/sample_rate)
# Bereken de sinusgolven voor elke toon met diepte van 2
# sine_0 = np.sin(2 * np.pi * np.arange(samples_per_tone) * freq_0 / sample_rate).astype(np.float32)
# sine_1 = np.sin(2 * np.pi * np.arange(samples_per_tone) * freq_1 / sample_rate).astype(np.float32)

sine_0 = np.sin(2*np.pi*freq_0*t)[:, np.newaxis]
sine_1 = np.sin(2*np.pi*freq_1*t)[:, np.newaxis]

# Initialisatie van Pygame
pygame.mixer.pre_init(sample_rate, -16, 2)
pygame.init()

# Functie om een toon af te spelen
# def play_tone(tone):
#     sound = pygame.sndarray.make_sound(tone)
#     sound.play()

# def play_tone(signal):
#     # Scale the signal to fit in the range of [-1, 1]
#     signal /= np.max(np.abs(signal))
    
#     # Repeat the signal for stereo output
#     signal = np.tile(signal, (2, 1)).T
    
#     # Play the sound using Pygame
#     sound = pygame.sndarray.make_sound(signal)
#     sound.play()
#     pygame.time.wait(int(duration*1000))

# def play_tone(frequency, duration, sample_rate):
#     # Generate the sine waves for 0 and 1
#     t = np.arange(0, duration, 1/sample_rate)
#     sine_0 = np.sin(2*np.pi*frequency*t)
#     sine_1 = np.sin(2*np.pi*(frequency + shift)*t)

#     # Combine the sine waves into a 2D array
#     signal = np.column_stack((sine_0, sine_1))

#     # Scale the signal to fit in the range of [-1, 1]
#     signal /= np.max(np.abs(signal))

#     # Repeat the signal for stereo output
#     signal = np.tile(signal, (2, 1)).T

#     # Create an audio segment from the signal
#     sound = pygame.sndarray.make_sound(signal)

#     # Play the audio segment and wait for it to finish
#     sound.play()
#     pygame.time.wait(int(duration*1000))

# def play_tone(frequency, duration, sample_rate, shift):
#     # Generate the sine waves for 0 and 1
#     t = np.arange(0, duration, 1/sample_rate)
#     sine_0 = np.sin(2*np.pi*frequency*t)
#     sine_1 = np.sin(2*np.pi*(frequency + shift)*t)

#     # Combine the sine waves into a 2D array
#     signal = np.column_stack((sine_0, sine_1))

#     # Scale the signal to fit in the range of [-1, 1]
#     signal /= np.max(np.abs(signal))

#     # Repeat the signal for stereo output
#     signal = np.tile(signal, (2, 1)).T

#     # Create an audio segment from the signal
#     sound = pygame.sndarray.make_sound(signal)

#     # Play the audio segment and wait for it to finish
#     sound.play()
#     pygame.time.wait(int(duration*1000))

def play_tone(frequency, duration, sample_rate, shift):
    # Generate the sine waves for 0 and 1
    t = np.arange(0, duration, 1/sample_rate)
    sine_0 = np.sin(2*np.pi*frequency*t)
    sine_1 = np.sin(2*np.pi*(frequency + shift)*t)

    # Combine the sine waves into a 2D array
    signal = np.column_stack((sine_0, sine_1))

    # Scale the signal to fit in the range of [-1, 1]
    signal /= np.max(np.abs(signal))

    # Convert the signal to a C-contiguous format
    signal = np.ascontiguousarray(signal)

    # Create an audio segment from the signal
    sound = pygame.sndarray.make_sound(signal)

    # Play the audio segment and wait for it to finish
    sound.play()
    pygame.time.wait(int(duration*1000))


# Functie om tekst naar RTTY-signaal te coderen en af te spelen
def send_message(msg):
    for c in msg:
        bits = baudot_table[c]
        for b in bits:
            if b == '0':
                play_tone(sine_0, duration, sample_rate, 170)
            else:
                play_tone(sine_1, duration, sample_rate, 170)
            time.sleep(duration)

# Test het verzenden van een bericht
send_message("HELLO WORLD\n")

play_tone(1000, 0.5, 44100, 170)