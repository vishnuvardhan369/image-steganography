#hiding rgb image in an RGB image

import cv2
import numpy as np

def encrypt(image1, image2, encrypted_image_name):
    cover_image = cv2.resize(cv2.imread(image1, 1), (800, 600))
    secret_image = cv2.resize(cv2.imread(image2, 1), (800, 600))

    for i in range(600):
        for j in range(800):
            for k in range(3):
                cover_image[i, j, k] = (cover_image[i, j, k] & 0xF0) | (secret_image[i, j, k] >> 4)

    cv2.imwrite(encrypted_image_name, cover_image)
    print(f"Successfully encrypted one image into another! Saved as {encrypted_image_name}")

def decrypt(encrypted_image_path, retrieved_image_name):
    encrypted_image = cv2.imread(encrypted_image_path, 1)
    retrieved_image = np.zeros_like(encrypted_image)

    for i in range(encrypted_image.shape[0]):
        for j in range(encrypted_image.shape[1]):
            for k in range(3):
                retrieved_image[i, j, k] = (encrypted_image[i, j, k] & 0x0F) << 4

    cv2.imwrite(retrieved_image_name, retrieved_image)
    print(f"Your image has been decrypted successfully! Saved as {retrieved_image_name}")

if __name__ == "__main__":
    e_or_d = int(input('''Do you want to encrypt or decrypt?
        Press 1 to ENCRYPT
        Press 2 to DECRYPT
        : '''))

    if e_or_d == 1:
        cover_image_path = input("Please enter the cover image: ")
        secret_image_path = input("Please enter the secret image to be encrypted: ")
        encrypted_image_name = input("Enter the name for the encrypted image (with extension .png): ")
        encrypt(cover_image_path, secret_image_path, encrypted_image_name)

    elif e_or_d == 2:
        encrypted_image_path = input("Please enter the encrypted image to decrypt: ")
        retrieved_image_name = input("Enter the name for the retrieved image (with extension .png): ")
        decrypt(encrypted_image_path, retrieved_image_name)

    else:
        print("Please restart and type in either 1 to encrypt an image or 2 to decrypt an image")
