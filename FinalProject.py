import pyttsx3
import PyPDF2
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import *
from ttkthemes import ThemedTk
import pathlib

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def read_file():
    file_path = file_path_var.get()

    # Check if the file path is not empty
    if file_path:
        # Setting audio properties
        engine.setProperty("volume", volume_scale.get())
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_var.get()].id)
        engine.setProperty('rate', speed_scale.get())

        file_ext = pathlib.Path(file_path).suffix

        if file_ext == ".pdf":
            read_pdf(file_path)
        elif file_ext != ".pdf":
            read_text(file_path)

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            engine.say(text)
            engine.runAndWait()

def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        engine.say(text)
        engine.runAndWait()

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)

def saveAudio():
    file_path = file_path_var.get()
    if file_path:
        text = ""
        file_ext = pathlib.Path(file_path).suffix
        if file_ext == ".pdf":
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        elif file_ext != ".pdf":
            with open(file_path, 'r') as file:
                text = file.read()

        if text.strip():
            filename = filedialog.asksaveasfilename(defaultextension=".wav")
            if filename:
                engine.save_to_file(text, filename)
                engine.runAndWait()
                messagebox.showinfo('Successful', 'Audio file saved')
            else:
                messagebox.showwarning('Error', 'Please select a file')

# Create the main GUI window

window = ThemedTk(theme="black")
window.configure(bg="wheat")
window.title("File Reader")

content = ttk.Frame(window, padding=20)

# Create file path variable
file_path_var = tk.StringVar()

# Create volume variable
volume_var = tk.StringVar(value=0.5)

# Speed scale variable
speed_scale = tk.IntVar(value=200)

# Create voice variable
voice_var = tk.IntVar(value=0)

# Heading
header = tk.Label(content, text="Welcome to my text to speech application,\n you can read PDF or text files out loud🔊, save the file ⬇, and change properties of the speech!\n ", bg="cyan", fg="black", justify="center", font="cursive, 12")

# File label
file_label = ttk.Label(content, text="\nSELECT FILE:")

# File input
file_entry = ttk.Entry(content, textvariable=file_path_var)

# Browse button
file_button = tk.Button(content, text="Browse", command=open_file_dialog, bg="#cccccc")

#SET PROPERTIES
Frame1= tk.Frame(content, relief=tk.SUNKEN)
props= ttk.Label(Frame1, text='SET PROPERTIES OF THE AUDIO')

Frame2= ttk.Frame(content, relief=tk.SUNKEN)
Frame2['padding'] = 8
# Volume label
volume_label = ttk.Label(Frame2, text="\nVolume (from 0.0 to 1.0):")

volume_scale = tk.Scale(Frame2, from_=0.0, to=1.0, orient=tk.HORIZONTAL, resolution=0.1, length=170, variable=volume_var, bg='#ffffff')

# Speed frame
speed_label = ttk.Label(Frame2, text="Change Speed (words per minute)")

# Speed scale
speed_scale_widget = tk.Scale(Frame2, from_=100, to=300, orient=tk.HORIZONTAL, length=170, variable=speed_scale, bg='#ffffff')

# Voice label
voice_label = ttk.Label(Frame2, text="Change Voice")

Male = tk.Radiobutton(Frame2, text='Male', variable=voice_var, value=0)

Female = tk.Radiobutton(Frame2, text='Female', variable=voice_var, value=1)

Frame3 = tk.Frame(content, relief=tk.SUNKEN)

# Read File button
read_button = tk.Button(Frame3, text="Read File", command=read_file, bg="green", fg='white')

# Pause Button
pause_button = tk.Button(Frame3, text="⏯️", bg="white", fg='white')

# Exit Button
exit_button = tk.Button(content, text="❌", command=window.quit, bg="red")

# Save file button
save_button = tk.Button(Frame3, text="Save Audio File as", command=saveAudio, bg="green", fg='white')


#-- GRID---
content.grid(row=0, column=0)
header.grid(column=0, row=1, columnspan=3)
file_label.grid(column=0, row=2)
file_entry.grid(column=0, row=3)
file_button.grid(column=0, row=4)

Frame1.grid(row=2, column=1, columnspan=3)
props.grid(row=0, column=0)

Frame2.grid(row=3, column=1, columnspan=3, rowspan=5)
#--FRAME 2--
volume_label.grid(column=1, row=2, columnspan=2)
volume_scale.grid(column=1, row=3, columnspan=2)
speed_label.grid(column=1, row=4, columnspan=2)
speed_scale_widget.grid(column=1, row=5, columnspan=2)
voice_label.grid(column=1, row=6, columnspan=2)
#--FRAME 4--
Male.grid(column=1, row=7)
Female.grid(column=2, row=7)

Frame3.grid(row=6, column=0)
#---FRAME 3 ---
read_button.grid(column=0, row=0)
pause_button.grid(column=1, row=0)
save_button.grid(column=2, row=0)
exit_button.grid(column=3, row=0)


window.mainloop()