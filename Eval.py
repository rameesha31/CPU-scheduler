from PIL import Image, ImageSequence, ImageTk
import tkinter as tk
import customtkinter as ctk
import subprocess
import sys
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sqlite3

# Function to retrieve data from database
def retrieve_last_five_algo_data():
    conn = sqlite3.connect('scheduling_algorithms.db')
    c = conn.cursor()

    # Get the IDs of the last five algorithms based on their IDs
    # Execute the query to get the last five distinct rows based on algo_name
    query = """
    WITH RankedAlgoPerformance AS (
        SELECT 
            id,
            algo_name,
            avg_turnaround_time,
            avg_waiting_time,
            ROW_NUMBER() OVER (PARTITION BY algo_name ORDER BY id DESC) as rn
        FROM 
            algo_performance
    )
    SELECT 
        id, algo_name, avg_turnaround_time, avg_waiting_time
    FROM 
        RankedAlgoPerformance
    WHERE 
        rn = 1
    ORDER BY 
        id DESC
    LIMIT 5;
    """
    c.execute(query)
    # c.execute("SELECT id FROM algo_performance ORDER BY id DESC LIMIT 5")
    last_five_ids = [row[0] for row in c.fetchall()]

    # Retrieve data for the last five algorithms
    c.execute("SELECT algo_name, avg_turnaround_time, avg_waiting_time FROM algo_performance WHERE id IN ({})".format(','.join(map(str, last_five_ids))))
    rows = c.fetchall()
    print(rows)

    conn.close()
    return rows




app=ctk.CTk()
app.geometry("1200x630+45+1")
app.resizable(False, False)
app.configure(fg_color="#002244")
gifImage = "eval.gif"
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

# Function to normalize and calculate performance score
def calculate_performance(data):
    max_turnaround_time = max(row[1] for row in data)
    max_waiting_time = max(row[2] for row in data)
    
    performance_scores = []
    for row in data:
        algo_name, avg_turnaround_time, avg_waiting_time = row
        normalized_turnaround = avg_turnaround_time / max_turnaround_time
        normalized_waiting = avg_waiting_time / max_waiting_time
        combined_score = normalized_turnaround + normalized_waiting
        performance_scores.append((algo_name, combined_score, avg_turnaround_time, avg_waiting_time))
    
    return sorted(performance_scores, key=lambda x: x[1])

# Function to draw pie chart
def draw_pie_chart(canvas, data):
    algorithms = [row[0] for row in data]
    scores = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(scores, labels=algorithms, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(scores))))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add a title
    plt.title("Performance Scores of Five Algorithms")

    # Embed the plot into the tkinter canvas
    pie_canvas = FigureCanvasTkAgg(fig, canvas)
    pie_canvas.draw()
    pie_canvas.get_tk_widget().pack()

def draw_bar_chart_turnaround(canvas, data):
    algorithms = [row[0] for row in data]
    avg_turnaround_times = [row[1] for row in data]
    max_time = max(avg_turnaround_times)

    bar_width = 20
    bar_spacing = 10
    chart_height = 200
    chart_width = 350
    x_offset = 30
    y_offset = 30

    title_text = "Average Turnaround Time for Five Algorithms"
    canvas.create_text(chart_width / 2 + x_offset, y_offset / 2, text=title_text, font=('Helvetica', 10, 'bold'), fill='black')

    canvas.create_rectangle(x_offset, y_offset, chart_width + x_offset, chart_height + y_offset, outline='black', fill='white')
    max_bar_length = chart_width - 2 * x_offset

    for i, (algo, turnaround_time) in enumerate(zip(algorithms, avg_turnaround_times)):
        bar_length = (turnaround_time / max_time) * max_bar_length  
        x0 = x_offset
        y0 = y_offset + i * (bar_width + bar_spacing)
        x1 = x_offset + bar_length
        y1 = y0 + bar_width

        canvas.create_rectangle(x0, y0, x1, y1, fill='skyblue', outline='black')
        canvas.create_text(x0 - 10, y0 + bar_width / 2, text=algo, anchor='e')
        canvas.create_text(x1 + 10, y0 + bar_width / 2, text=f'{turnaround_time:.2f}', anchor='w')

def draw_bar_chart_waiting(canvas, data):
    algorithms = [row[0] for row in data]
    avg_waiting_times = [row[2] for row in data]
    max_time = max(avg_waiting_times)

    bar_width = 20
    bar_spacing = 10
    chart_height = 200
    chart_width = 350
    x_offset = 30
    y_offset = 30

    title_text = "Average Waiting Time for Five Algorithms"
    canvas.create_text(chart_width / 2 + x_offset, y_offset / 2, text=title_text, font=('Helvetica', 10, 'bold'), fill='black')

    canvas.create_rectangle(x_offset, y_offset, chart_width + x_offset, chart_height + y_offset, outline='black', fill='white')
    max_bar_length = chart_width - 2 * x_offset

    for i, (algo, wait_time) in enumerate(zip(algorithms, avg_waiting_times)):
        bar_length = (wait_time / max_time) * max_bar_length  
        x0 = x_offset
        y0 = y_offset + i * (bar_width + bar_spacing)
        x1 = x_offset + bar_length
        y1 = y0 + bar_width

        canvas.create_rectangle(x0, y0, x1, y1, fill='skyblue', outline='black')
        canvas.create_text(x0 - 10, y0 + bar_width / 2, text=algo, anchor='e')
        canvas.create_text(x1 + 10, y0 + bar_width / 2, text=f'{wait_time:.2f}', anchor='w')




def animation():
    global count, showAnimation, is_playing
    if is_playing:
        gif_Label.configure(image=frames[count])
        count += 1
        if count == len(frames)-100:
            is_playing = False

            

            def simulate():
                app.destroy()
                subprocess.run([sys.executable, 'agenda.py'])

            simulate_button=ctk.CTkButton(gif_Label,width=15,height=30,image=my_image,text="", corner_radius=50, fg_color="#F64A8A",bg_color="#662d91", hover_color="#662d91",command=simulate)
            simulate_button.place(relx=0.95, rely=0.1, anchor="center")

            # Retrieve data and draw bar chart
            data = retrieve_last_five_algo_data()
            performance_data = calculate_performance(data)
            
            canvas1 = tk.Canvas(gif_Label, width=400, height=250, bg='#ff007e')
            canvas1.place(relx=0.3, rely=0.4, anchor="center")
            draw_bar_chart_turnaround(canvas1, data)
            
            canvas2 = tk.Canvas(gif_Label, width=400, height=250, bg='#ff007e')
            canvas2.place(relx=0.3, rely=0.8, anchor="center")
            draw_bar_chart_waiting(canvas2, data)
            
            canvas3 = tk.Canvas(gif_Label, width=400, height=250,bg='#ff007e')
            canvas3.place(relx=0.7, rely=0.6, anchor="center")
            draw_pie_chart(canvas3, performance_data)

            
            
        else:
            showAnimation = app.after(50, animation)

    

# Set the size of the label to the size of the first frame
gif_Label = tk.Label(app, image=frames[0])
gif_Label.place(x=0, y=0, width=frames[0].width(), height=frames[0].height())

animation()



app.mainloop()