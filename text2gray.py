#hiding text in a grayscale image

import cv2
import os

def str_to_binary(string):
    return ''.join(format(ord(char), '08b') for char in string)

def binary_to_string(binary_data):
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def get_pattern(height, width, pattern):
    if pattern == "horizontal":
        return [(i, j) for i in range(height) for j in range(width)]
    elif pattern == "vertical":
        return [(j, i) for i in range(width) for j in range(height)]
    elif pattern == "diagonal":
        return [(i, i) for i in range(min(height, width))]
    elif pattern == "checkerboard":
        return [(i, j) for i in range(height) for j in range(width) if (i + j) % 2 == 0]
    elif pattern == "zigzag":
        return [(i, j) if i % 2 == 0 else (i, width - j - 1) for i in range(height) for j in range(width)]
    else:
        print("Invalid pattern. Using the default pattern (horizontal).")
        return [(i, j) for i in range(height) for j in range(width)]

def encrypt(image_path, message, password, pattern, encrypted_image_name):
    if not os.path.isfile(image_path):
        print("Error: The specified file does not exist.")
        return

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Error: Unable to load the image. Please check the file path.")
        return

    bin_message = str_to_binary(message)

    bin_to_hide = str_to_binary(password) + bin_message + str_to_binary(password)

    height, width = img.shape
    pattern_positions = get_pattern(height, width, pattern)

    t = 0
    for i, j in pattern_positions:
        if t < len(bin_to_hide):
            img[i, j] = (img[i, j] & 0b11111110) | int(bin_to_hide[t])
            t += 1

    cv2.imwrite(encrypted_image_name, img)

    print(f"Successfully encrypted! Saved as {encrypted_image_name}")

def decrypt(image_path, password, pattern):
    if not os.path.isfile(image_path):
        print("Error: The specified file does not exist.")
        return None

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Error: Unable to load the image. Please check the file path.")
        return None

    height, width = img.shape
    pattern_positions = get_pattern(height, width, pattern)

    bin_data = ''
    for i, j in pattern_positions:
        bin_data += str(img[i, j] & 1)

    password_index = bin_data.find(str_to_binary(password))
    if password_index == -1:
        print("Invalid password. Decryption failed.")
        return None

    if password_index % 8 != 0:
        print("Invalid password. Decryption failed.")
        return None

    bin_message = bin_data[password_index + len(str_to_binary(password)):]

    end_index = bin_message.find(str_to_binary(password))
    if end_index == -1:
        print("Invalid password. Decryption failed.")
        return None

    bin_message = bin_message[:end_index]

    return binary_to_string(bin_message)

if __name__ == "__main__":
    e_or_d = int(input('''Do you want to encrypt or decrypt?
        press 1 to ENCRYPT
        press 2 to DECRYPT
        : '''))

    if e_or_d == 1:
        image = input("Enter the image to encrypt your message in: ")
        message = input("Enter the message to encrypt: ")
        pattern = input("Enter the pattern (horizontal, vertical, diagonal, checkerboard, zigzag): ")
        encrypted_image_name = input("Enter the name for the encrypted image (with extension .png): ")
        password = input("Enter the password: ")
        encrypt(image, message, password, pattern, encrypted_image_name)

    elif e_or_d == 2:
        image = input("Enter the image to decrypt your message from: ")
        password = input("Enter the password: ")
        pattern = input("Enter the pattern (horizontal, vertical, diagonal, checkerboard, zigzag): ")
        decrypted_message = decrypt(image, password, pattern)
        if decrypted_message is not None:
            print("Successfully decrypted!")
            print("Decrypted message:", decrypted_message)
        else:
            print("Decryption failed.")

    else:
        print("Please restart and type in either 1 to encrypt or 2 to decrypt")
