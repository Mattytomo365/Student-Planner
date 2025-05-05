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

# Screen header

header = tk.Label(main, text="Day of the week", font=("Arial", 40), bg="white", fg="green")
header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=250, pady=5)

# Daily checklist

events = get_upcoming_events(creds)
checklist = tk.Listbox(main, width=40, height=20, bg="white", fg="black", highlightbackground="black", highlightthickness=1)

for summary in events:
    checklist.insert(tk.END, summary)

checklist.grid(row=1, column=0, sticky="nsw", padx=20, pady=50, rowspan=2)

# Progress bar

progress = ttk.Progressbar(main, orient="horizontal", length=365, mode="determinate")
progress.grid(row=3, column=0, sticky="nsw", padx=20, pady=0)

# Buttons

task_actions_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=2)
task_actions_frame.grid(row=1, column=1, sticky="nsw", padx=10, pady=50)

task_header = tk.Label(task_actions_frame, text="Task Actions", font=("Arial", 20), bg="white", fg="black")
task_header.grid(row=0, column=1, padx=10, pady=10)

add_button = tk.Button(task_actions_frame, text="Add Task", bg="white", fg="black")
add_button.grid(row=1, column=1, padx=10, pady=10)

edit_button = tk.Button(task_actions_frame, text="Edit Task", bg="white", fg="black")
edit_button.grid(row=1, column=2, padx=10, pady=10)

delete_button = tk.Button(task_actions_frame, text="Delete Task", bg="white", fg="black")
delete_button.grid(row=2, column=1, padx=10, pady=10)

other_action_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=2)
other_action_frame.grid(row=2, column=1, sticky="nsw", padx=10, pady=50)

other_header = tk.Label(other_action_frame, text="Other Actions", font=("Arial", 20), bg="white", fg="black")
other_header.grid(row=0, column=1, padx=10, pady=10)

add_assignment_button = tk.Button(other_action_frame, text="Add Assignment", bg="white", fg="black")
add_assignment_button.grid(row=1, column=1, padx=10, pady=10)

view_key_button = tk.Button(other_action_frame, text="View Key", bg="white", fg="black")
view_key_button.grid(row=1, column=2, padx=10, pady=10)

main.mainloop()