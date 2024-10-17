from PIL import Image, ImageSequence, ImageTk
import tkinter as tk
import customtkinter as ctk
import subprocess
import sys
import sqlite3

# Connect to the SQLite database or create it if it doesn't exist
conn = sqlite3.connect('scheduling_algorithms.db')
c = conn.cursor()

# Create a table to store algorithm performance if it doesn't exist already
c.execute('''CREATE TABLE IF NOT EXISTS algo_performance (
             id INTEGER PRIMARY KEY,
             algo_name TEXT,
             avg_turnaround_time REAL,
             avg_waiting_time REAL)''')

# Commit the changes and close the connection
conn.commit()


app=ctk.CTk()
app.geometry("1100x630+45+1")
app.resizable(False, False)
app.configure(fg_color="#ffffff")
gifImage = "Project Proposal Presentation (3).gif"
openImage = Image.open(gifImage)
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(openImage)]

count = 0
showAnimation = None
is_playing = True  # Flag to control animation

# Load an image of equipment----------------------------------------------------------------------------------------------------------
my_image = ctk.CTkImage(
        light_image=Image.open("icons8-fast-forward-64.png"),
        dark_image=Image.open("icons8-fast-forward-64.png"),
        size=(30, 50),
    )

def animation():
    global count, showAnimation, is_playing
    if is_playing:
        gif_Label.configure(image=frames[count])
        count += 1
        if count == len(frames)-1:
            is_playing = False
            def simulate():
                app.destroy()
                subprocess.run([sys.executable, 'EnterFile.py'])

            simulate_button=ctk.CTkButton(gif_Label,width=70,height=60,image=my_image,anchor="w",compound="left",text="Continue... ", corner_radius=35, fg_color="#F64A8A",bg_color="#FFFFFF", hover_color="#662d91",command=simulate)
            simulate_button.place(relx=0.85, rely=0.91, anchor="center")
        else:
            showAnimation = app.after(50, animation)

    

# Set the size of the label to the size of the first frame
gif_Label = tk.Label(app, image=frames[0])
gif_Label.place(x=0, y=0, width=frames[0].width(), height=frames[0].height())

animation()



app.mainloop()