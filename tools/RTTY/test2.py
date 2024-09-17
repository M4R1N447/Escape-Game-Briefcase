import numpy as np
import pyaudio
import wave
import struct

# Het baudot alfabet
baudot_code = {
    '00000': ' ', '00001': 'E', '00010': '\n', '00011': 'A',
    '00100': ' ', '00101': 'S', '00110': 'I', '00111': 'U',
    '01000': ' ', '01001': 'D', '01010': 'R', '01011': 'J',
    '01100': 'K', '01101': 'L', '01110': 'M', '01111': 'N',
    '10000': 'O', '10001': 'Q', '10010': 'R', '10011': 'S',
    '10100': 'T', '10101': 'U', '10110': 'V', '10111': '_',
    '11000': 'X', '11001': 'Y', '11010': 'Z', '11011': '\n',
    '11100': '.', '11101': ',', '11110': '-', '11111': ':',
}

# Functie voor het encoderen van een bericht
def baudot_encode(message):
    encoded = ''
    for char in message.upper():
        code = [k for k, v in baudot_code.items() if v == char]
        if code:
            encoded += code[0]
    return encoded

# Functie voor het decoderen van een bericht
def baudot_decode(encoded):
    decoded = ''
    while len(encoded) >= 5:
        char = encoded[:5]
        encoded = encoded[5:]
        decoded += baudot_code.get(char, '')
    return decoded

# Functie voor het genereren van een toon
def generate_tone(freq, duration, amplitude, sample_rate):
    wave_data = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        sample = amplitude * np.sin(2 * np.pi * freq * i / sample_rate)
        wave_data.append(sample)
    return wave_data

# Functie voor het maken van een WAV-bestand
def create_wav_file(filename, sample_rate, wave_data):
    wav_file = wave.open(filename, 'wb')
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for sample in wave_data:
        wav_file.writeframes(struct.pack('h', int(sample)))
    wav_file.close()

# Functie voor het afspelen van een WAV-bestand
def play_wav_file(filename):
    wav_file = wave.open(filename, 'rb')
    player = pyaudio.PyAudio()
    stream = player.open(
        format=player.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True
    )
    data = wav_file.readframes(1024)
    while data:
        stream.write(data)
        data = wav_file.readframes(1024)
    stream.stop_stream()
    stream.close()
    player.terminate()

# De frequenties van de mark- en space-signalen
mark_freq = 2125
space_freq = 2295

# De duur van elk signaal in seconden
signal_duration = 0.1

# De sample rate van het audio-bestand
sample_rate = 44100

# Het bericht dat we willen encoderen en decoderen
message = "Hello world!"

#Encoderen van het bericht
encoded_message = baudot_encode(message)

#Decoded het gecodeerde bericht
decoded_message = baudot_decode(encoded_message)

#Printen van de oorspronkelijke boodschap en de gedecodeerde boodschap
print(f"Oorspronkelijke bericht: {message}")
print(f"Gecodeerde bericht: {encoded_message}")
print(f"Gedecodeerde bericht: {decoded_message}")

#Genereren van de mark- en space-tonen
mark_tone = generate_tone(mark_freq, signal_duration, 0.5, sample_rate)
space_tone = generate_tone(space_freq, signal_duration, 0.5, sample_rate)

#Genereren van de golfvorm voor het gecodeerde bericht
wave_data = []
for char in encoded_message:
    if char == ' ':
        wave_data.extend(generate_tone(space_freq, signal_duration, 0.5, sample_rate))
    else:
        code = char * 2
    for i in range(0, len(code), 2):
        if code[i:i+2] == '10':
            wave_data.extend(generate_tone(mark_freq, signal_duration, 0.5, sample_rate))
        else:
            wave_data.extend(generate_tone(space_freq, signal_duration, 0.5, sample_rate))

#Aanmaken van de WAV-bestanden voor de mark- en space-tonen
create_wav_file('mark.wav', sample_rate, mark_tone)
create_wav_file('space.wav', sample_rate, space_tone)

#Aanmaken van de WAV-bestand voor het gecodeerde bericht
create_wav_file('message.wav', sample_rate, wave_data)

#Afspelen van de mark- en space-tonen en het gecodeerde bericht
play_wav_file('mark.wav')
play_wav_file('space.wav')
play_wav_file('message.wav')
