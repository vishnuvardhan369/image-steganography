import wave
from PIL import Image
import numpy as np

def audio_to_binary(audio_file):
    with wave.open(audio_file, 'rb') as audio:
        audio_frames = audio.readframes(audio.getnframes())
        binary_sequence = ''.join(format(byte, '08b') for byte in audio_frames)

    return binary_sequence, audio.getframerate(), audio.getsampwidth(), audio.getnchannels()

def ascii_to_binary(password):
    return ''.join(format(ord(char), '08b') for char in password)

def binary_to_audio(binary_data, output_audio_file, sample_rate, sample_width, num_channels):
    byte_array = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

    with wave.open(output_audio_file, 'wb') as audio:
        audio.setnchannels(num_channels)
        audio.setsampwidth(sample_width)
        audio.setframerate(sample_rate)
        audio.writeframes(byte_array)

def encrypt_audio(audio_file_path, image_file_path, output_image_file_path, password):
    binary_data, sample_rate, sample_width, num_channels = audio_to_binary(audio_file_path)

    # Convert password to ASCII values and add it to the beginning of the binary data
    password_binary = ascii_to_binary(password)
    binary_data = password_binary + binary_data

    # Open the image for embedding
    img = Image.open(image_file_path)
    pixels = np.array(img)

    # Embed audio data in the least significant bit of each pixel
    binary_index = 0
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            for k in range(len(pixels[i][j])):
                if binary_index < len(binary_data):
                    pixels[i][j][k] = (pixels[i][j][k] & 0xFE) | int(binary_data[binary_index])
                    binary_index += 1

    # Save the modified image with audio metadata
    img = Image.fromarray(pixels)
    img.info['fps'] = sample_rate
    img.info['sampwidth'] = sample_width
    img.info['nchannels'] = num_channels
    img.save(output_image_file_path)

    # Display audio parameters
    print("Audio Parameters:")
    print("Sample Rate:", sample_rate, "Hz")
    print("Sample Width:", sample_width, "bytes")
    print("Number of Channels:", num_channels)

    print("Encryption complete!")

def decrypt_audio(image_file_path, output_audio_file_path):
    img = Image.open(image_file_path)
    pixels = np.array(img)

    binary_data = ''
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            for k in range(len(pixels[i][j])):
                binary_data += str(pixels[i][j][k] & 1)

    # Find the position of the first '1' in the binary data
    start_index = binary_data.find('1')

    # Extract the original binary data (excluding the password part)
    original_binary_data = binary_data[start_index:]

    # Convert password part to ASCII
    password_binary = original_binary_data[:start_index]
    password = ''.join([chr(int(password_binary[i:i+8], 2)) for i in range(0, len(password_binary), 8)])

    # Display password
    print("Decryption successful!")
    print("Password:", password)

    # Ask the user for audio parameters
    sample_rate = int(input("Enter the sample rate: "))
    sample_width = int(input("Enter the sample width (in bytes): "))
    num_channels = int(input("Enter the number of channels: "))

    # Convert binary sequence to audio
    binary_to_audio(original_binary_data, output_audio_file_path, sample_rate, sample_width, num_channels)

# Rest of the code remains unchanged

# User Input
choice = int(input("Enter 1 for encryption or 2 for decryption: "))

if choice == 1:
    input_audio_file_path = input("Enter the path of the input audio file: ")
    input_image_file_path = input("Enter the path of the input image file: ")
    output_image_file_path = input("Enter the path for the output image file: ")
    password = input("Enter the password for encryption: ")
    encrypt_audio(input_audio_file_path, input_image_file_path, output_image_file_path, password)
elif choice == 2:
    input_image_file_path = input("Enter the path of the input image file with hidden audio: ")
    output_audio_file_path = input("Enter the path for the output audio file: ")
    decrypt_audio(input_image_file_path, output_audio_file_path)
else:
    print("Invalid choice. Please enter 1 for encryption or 2 for decryption.")
