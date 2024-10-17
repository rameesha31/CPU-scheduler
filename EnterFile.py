#ff007e
from PIL import Image, ImageSequence, ImageTk
import tkinter as tk
import customtkinter as ctk
import subprocess
import sys
import sqlite3

# Connect to the SQLite database or create it if it doesn't exist
conn = sqlite3.connect('file_paths.db')
c = conn.cursor()

# Create a table to store file paths if it doesn't exist already
c.execute('''CREATE TABLE IF NOT EXISTS file_path
             (id INTEGER PRIMARY KEY, path TEXT)''')




app=ctk.CTk()
app.geometry("1100x630+45+1")
app.resizable(False, False)
app.configure(fg_color="#002244")
gifImage = "Project Proposal Presentation (5).gif"
openImage = Image.open(gifImage)
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(openImage)]

count = 0
showAnimation = None
is_playing = True  # Flag to control animation

# Load an image of equipment----------------------------------------------------------------------------------------------------------
my_image = ctk.CTkImage(
        light_image=Image.open("icons8-fast-forward-64.png"),
        dark_image=Image.open("icons8-fast-forward-64.png"),
        size=(15, 30),
    )

def animation():
    global count, showAnimation, is_playing
    if is_playing:
        gif_Label.configure(image=frames[count])
        count += 1
        if count == len(frames)-110:
            is_playing = False
            # Create a custom font for the placeholder text and button text
            custom_font = ("Helvetica", 20, "bold")
            # name entry field
            name_entry = ctk.CTkEntry(gif_Label, placeholder_text="e.g processes.csv ", width=500, height=50, fg_color="#ff007e",bg_color="#ff007e", border_width=0, text_color="white")
            name_entry.place(relx=0.90, rely=0.40, anchor="e")
            name_entry.configure(font=custom_font)
            # name underline
            name_line = ctk.CTkFrame(gif_Label, width=500, height=3, fg_color="white")
            name_line.place(relx=0.90, rely=0.45, anchor="e")

            #submission button
            def submit():
                file = name_entry.get()
                # Insert the file path into the database
                c.execute("INSERT INTO file_path (path) VALUES (?)", (file,))
                conn.commit()
                print(f"File path submitted: {file}")
                app.destroy()
                subprocess.run([sys.executable, 'evaluation.py'])
                

            submit_button=ctk.CTkButton(gif_Label,width=250,height=65,compound="left",text="Submit File ", corner_radius=50, fg_color="#ff007e",bg_color="#ff007e", hover_color="#662d91",command=submit)
            submit_button.place(relx=0.71, rely=0.60, anchor="center")
            submit_button.configure(font=custom_font)

            def back():
             app.destroy()
             subprocess.run([sys.executable, 'agenda.py'])

            back_button=ctk.CTkButton(gif_Label,width=15,height=30,image=my_image,text="", corner_radius=50, fg_color="#F64A8A",bg_color="#0200d6", hover_color="#662d91",command=back)
            back_button.place(relx=0.93, rely=0.89, anchor="center")
        else:
            showAnimation = app.after(50, animation)

    

# Set the size of the label to the size of the first frame
gif_Label = tk.Label(app, image=frames[0])
gif_Label.place(x=0, y=0, width=frames[0].width(), height=frames[0].height())



animation()



app.mainloop()