from PIL import Image, ImageSequence, ImageTk
import tkinter as tk
import customtkinter as ctk
import subprocess
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from first import Process, read_processes_from_dataframe,round_robin_scheduling, evaluate_performance

def insert_performance_data(algo_name, avg_turnaround_time, avg_waiting_time):
    conn = sqlite3.connect('scheduling_algorithms.db')
    c = conn.cursor()
    
    # Insert data into the table
    c.execute("INSERT INTO algo_performance (algo_name, avg_turnaround_time, avg_waiting_time) VALUES (?, ?, ?)",
              (algo_name, avg_turnaround_time, avg_waiting_time))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Connect to the SQLite database
conn = sqlite3.connect('file_paths.db')
c = conn.cursor()

# Retrieve the latest file path from the database
c.execute("SELECT path FROM file_path ORDER BY id DESC LIMIT 1")
result = c.fetchone()
if result:
    file_path = result[0]
    print(f"File path received: {file_path}")
else:
    print("No file path found in the database")

# Close the connection to the database
conn.close()

#making dataframe of the file
df = pd.read_csv(file_path)
# print(df)

processes = read_processes_from_dataframe(df)

   
tab_count = 0
tab_showAnimation = None
tab_isplaying = True


app=ctk.CTk()
app.geometry("1100x630+45+1")
app.resizable(False, False)
app.configure(fg_color="#002244")
gifImage = "Project Proposal Presentation (6).gif"
openImage = Image.open(gifImage)
# Load an image of equipment----------------------------------------------------------------------------------------------------------

frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(openImage)]

    
    # Dictionary to store frames for each tab
tab_frames = {}

    # Function to load frames for each tab
def load_tab_frames(tab_name, gif_path):
        openImage = Image.open(gif_path)
        tab_frames[tab_name] = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(openImage)]


# Load an image of equipment----------------------------------------------------------------------------------------------------------
my_image = ctk.CTkImage(
        light_image=Image.open("icons8-fast-forward-64.png"),
        dark_image=Image.open("icons8-fast-forward-64.png"),
        size=(15, 30),
    )
    # Function to handle animation for each tab
def tab_animation(tab_name, gif_Label, scheduled_processes):
        global tab_count, tab_showAnimation, tab_isplaying
        frames = tab_frames[tab_name]

        def animate():
            global tab_count, tab_showAnimation, tab_isplaying
            if tab_isplaying and tab_count < len(frames):
                gif_Label.configure(image=frames[tab_count])
                tab_count += 1
                if tab_count == len(frames)-1:
                    tab_isplaying = False

                    # Create a canvas for the Gantt chart
                    canvas = tk.Canvas(tab, width=700, height=400, bg='#ff007e')
                    canvas.place(relx=0.65, rely=0.5, anchor="center")
                    max_end_time = max(process.end_time for process in scheduled_processes)
                    #Draw Gantt bars
                    for i, process in enumerate(scheduled_processes):
                        x0 = process.start_time * (680 / max(process.end_time for process in scheduled_processes))
                        y0 = 10 * (i + 1) - 5
                        x1 = process.end_time * (680 / max(process.end_time for process in scheduled_processes))
                        y1 = y0 + 50 # Increased height of rectangles
                        canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                        canvas.create_text((x0 + x1) / 2, y0 + 7, text=f'P{process.pid}')
                        canvas.create_text(x0, y1 + 5, text=str(process.start_time), anchor="n", fill="white")  # Start time label
                        canvas.create_text(x1, y1 + 5, text=str(process.end_time), anchor="n", fill="white")  # End time labe
                    
                    
                                        
                    def next():
                        app.destroy()
                        subprocess.run([sys.executable, 'PS.py'])

                    next_button=ctk.CTkButton(tab,width=15,height=30,image=my_image,text="", corner_radius=50, fg_color="#F64A8A",bg_color="white", hover_color="#662d91",command=next)
                    next_button.place(relx=0.95, rely=0.95, anchor="center")

                    def back():
                        app.destroy()
                        subprocess.run([sys.executable, 'sjf.py'])

                    back_button=ctk.CTkButton(tab,width=5,height=30,text="", corner_radius=50, fg_color="#F64A8A",bg_color="white", hover_color="#662d91",command=back)
                    back_button.place(relx=0.04, rely=0.94, anchor="center")
                else:
                    tab_showAnimation = app.after(50, animate)
            else:
              if tab_showAnimation is not None:
                app.after_cancel(tab_showAnimation)
                tab_showAnimation = None
        animate()




scheduled_processes1 = round_robin_scheduling(processes)

avg_turnaround_time, avg_waiting_time = evaluate_performance(scheduled_processes1)
insert_performance_data("RR", avg_turnaround_time, avg_waiting_time)
                
scheduled_processes=[scheduled_processes1]
                # Move tab creation outside of animation function
tab_view = ctk.CTkTabview(app, width=1060, height=590, bg_color="#002244", fg_color="#002244")
tab_view.pack(pady=5, padx=0, fill="both", expand=True)

                # Add named tabs and set up animations
tabs = []
tab_names = ["Round Robin"]  # Add more tab names here
gif_paths = [
                    "RR.gif"
                ]  # Add more gif paths here
for tab_name in tab_names:
        tab = tab_view.add(tab_name)
        tabs.append(tab)
        print(tabs)

tab_gif_label=[]
for tab in tabs:
        Label = tk.Label(tab)
        Label.pack(fill="both", expand=True)
        tab_gif_label.append(Label)
                    
                     
for tab, tab_name,label, gif_path, scheduled_process in zip(tabs, tab_names,tab_gif_label, gif_paths, scheduled_processes):
        load_tab_frames(tab_name, gif_path)  # Load frames for each tab
        tab_animation(tab_name, label, scheduled_process)



app.mainloop()

