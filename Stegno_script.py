import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# ASCII conversion dictionaries
d = {chr(i): i for i in range(256)}
c = {i: chr(i) for i in range(256)}

# Main functions
def encrypt_image(image_path, message, key):
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Image not found.")
        return

    n, m, z = x.shape
    if len(message) > (n * m):
        messagebox.showerror("Error", "Message too long for this image.")
        return

    # Store message length in first 4 pixels
    for i in range(4):
        x[0, i, 0] = (len(message) >> (i * 8)) & 0xFF

    index = 4
    kl = 0
    for ch in message:
        row = index // m
        col = index % m
        x[row, col, 0] = d[ch] ^ d[key[kl]]
        kl = (kl + 1) % len(key)
        index += 1

    cv2.imwrite("encrypted.png", x)
    messagebox.showinfo("Success", "Message successfully hidden in 'encrypted.png'")
    os.startfile("encrypted.png")

def decrypt_image(image_path, key):
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Image not found.")
        return

    n, m, z = x.shape

    msg_len = 0
    for i in range(4):
        msg_len |= x[0, i, 0] << (i * 8)

    index = 4
    kl = 0
    decrypt = ""
    for _ in range(msg_len):
        row = index // m
        col = index % m
        val = x[row, col, 0]
        decrypt += c[val ^ d[key[kl]]]
        kl = (kl + 1) % len(key)
        index += 1

    messagebox.showinfo("Extracted Message", decrypt)

# GUI Setup
def browse_image():
    filename = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filename)

def run_encrypt():
    encrypt_image(entry_image.get(), entry_message.get(), entry_key.get())

def run_decrypt():
    decrypt_image(entry_image.get(), entry_key.get())

root = tk.Tk()
root.title("Image Steganography Tool")

tk.Label(root, text="Select Image:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_image = tk.Entry(root, width=40)
entry_image.grid(row=0, column=1, padx=10)
tk.Button(root, text="Browse", command=browse_image).grid(row=0, column=2)

tk.Label(root, text="Message:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_message = tk.Entry(root, width=40)
entry_message.grid(row=1, column=1, padx=10)

tk.Label(root, text="Key:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_key = tk.Entry(root, width=40)
entry_key.grid(row=2, column=1, padx=10)

tk.Button(root, text="Encrypt", command=run_encrypt, bg="lightblue").grid(row=3, column=0, pady=10)
tk.Button(root, text="Decrypt", command=run_decrypt, bg="lightgreen").grid(row=3, column=1, pady=10)

root.mainloop()
