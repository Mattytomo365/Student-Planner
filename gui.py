import tkinter as tk
from tkinter import ttk
from logic import *
from main import *

main = tk.Tk()

main.geometry("800x600")
main.title("My GUI")
main.configure(bg="white")
main.resizable(False, False)

creds = authentication()

style = ttk.Style(main)
style.theme_use("clam")  # Change theme to allow background color changes
style.configure("Green.TButton",
                background="green",
                foreground="white",
                font=("Helvetica", 12),
                padding=6)
style.configure("Green.Horizontal.TProgressbar", 
                troughcolor="white",
                background="green",
                foreground="green",
                bordercolor="black",)

# Screen header

header = tk.Label(main, text="Day of the week", font=("Arial", 40), bg="white", fg="green")
header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=250, pady=5)

# Daily checklist

events = get_upcoming_events(creds)

checklist_frame = tk.Frame(main, width=30, height=20, bg = "white", highlightbackground="green", highlightthickness=1)
checklist_frame.grid(row=1, column=0, sticky="nsw", padx=20, pady=50, rowspan=2)

checklist_header = tk.Label(checklist_frame, text="To-Do", font=("Arial", 20), bg="white", fg="green")
checklist_header.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

task_vars = []

for summary in events:
    var = tk.BooleanVar()
    task_vars.append(var)
    checkbox = tk.Checkbutton(checklist_frame, text=summary, variable=var, bg="white", fg="black", width=30, justify="left", anchor="w", selectcolor="green", padx=30)
    checkbox.grid(row=len(task_vars), column=0, sticky="nsw", padx=30, pady=5)

# Progress bar

progress = ttk.Progressbar(main, orient="horizontal", length=400, mode="determinate", style="Green.Horizontal.TProgressbar")
progress["value"] = 50
progress.grid(row=3, column=0, sticky="nsw", padx=20, pady=0)

# Buttons

task_actions_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
task_actions_frame.grid(row=1, column=1, sticky="nsw", padx=10, pady=50)

task_header = tk.Label(task_actions_frame, text="Task Actions", font=("Arial", 20), bg="white", fg="black")
task_header.grid(row=0, column=1, padx=10, pady=10)

add_button = ttk.Button(task_actions_frame, text="Add Task", style="Green.TButton")
add_button.grid(row=1, column=1, padx=10, pady=10)

edit_button = ttk.Button(task_actions_frame, text="Edit Task", style="Green.TButton")
edit_button.grid(row=1, column=2, padx=10, pady=10)

delete_button = ttk.Button(task_actions_frame, text="Delete Task", style="Green.TButton")
delete_button.grid(row=2, column=1, padx=10, pady=10)

other_action_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
other_action_frame.grid(row=2, column=1, sticky="nsw", padx=10, pady=50)

other_header = tk.Label(other_action_frame, text="Other Actions", font=("Arial", 20), bg="white", fg="black")
other_header.grid(row=0, column=1, padx=10, pady=10)

add_assignment_button = ttk.Button(other_action_frame, text="Add Assignment", style="Green.TButton")
add_assignment_button.grid(row=1, column=1, padx=10, pady=10)

view_key_button = ttk.Button(other_action_frame, text="View Key", style="Green.TButton")
view_key_button.grid(row=1, column=2, padx=10, pady=10)

main.mainloop()