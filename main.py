import tkinter
import os
import sys
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    global img_name
    global img
    global submit

    img_name = filedialog.askopenfilename(
        initialdir=".",
        title="Select Image",
        filetypes=(("images", "*.jpg"), ("images", "*.bmp"), ("images", "*.png"))
    )

    if img_name:
        input_path.delete(0, tkinter.END)
        input_path.insert(0, img_name)
        label_original.grid(column=0, row=2)
        img = ImageTk.PhotoImage(Image.open(img_name).resize((250, 250)))
        original_image_label.configure(image=img)
        original_image_label.image = img
        original_image_label.grid(column=0, row=3)
        submit = tkinter.Button(root, text="Submit", command=call_haze)
        submit.grid(column=0, row=4)

def call_haze():
    global dehazed

    submit.destroy()  # Remove the submit button
    subprocess.call(f"python haze_removal.py \"{img_name}\"", shell=True)

    # Check if the output file exists
    if os.path.exists("img/dst.jpg"):
        msg = tkinter.Label(root, text="Dehazing complete! Image stored in dehazed folder.")
        msg.grid(column=0, row=4, columnspan=2)

        label_dehazed.grid(column=1, row=2)
        dehazed = ImageTk.PhotoImage(Image.open("img/dst.jpg").resize((250, 250)))
        dehazed_image_label.configure(image=dehazed)
        dehazed_image_label.image = dehazed
        dehazed_image_label.grid(column=1, row=3, padx=10)

        retry = tkinter.Button(root, text="Retry", command=restart_program)
        retry.grid(column=0, row=5)

        quit_button = tkinter.Button(root, text="Quit", command=quit_program)
        quit_button.grid(column=1, row=5)
    else:
        error_msg = tkinter.Label(root, text="Error: Dehazed image not found. Please try again.")
        error_msg.grid(column=0, row=5, columnspan=2)

def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)

def quit_program():
    sys.exit()

root = tkinter.Tk()
root.title("Dehaze")
root.update_idletasks()

label = tkinter.Label(root, text="Select image or enter image path:")
label.grid(column=0, row=0)

input_path = tkinter.Entry(root, width=50)
input_path.grid(column=0, row=1, padx=10, pady=10)

browse = tkinter.Button(root, text="Browse", command=open_image)
browse.grid(column=1, row=1)

label_original = tkinter.Label(root, text="Original Image:")
original_image_label = tkinter.Label(root)
label_dehazed = tkinter.Label(root, text="Dehazed Image:")
dehazed_image_label = tkinter.Label(root)

root.mainloop()


















