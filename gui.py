import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from logic import *
from main import *


class StudentPlannerApp:
    def __init__(self, main):
        self.main = main
        self.main.geometry("800x600")
        self.main.title("My GUI")
        self.main.configure(bg="white")
        self.main.resizable(False, False)

        self.creds = authentication()
        self.task_vars = []

        self.setup_styles()
        self.build_main_window()
    
    def setup_styles(self):
        style = ttk.Style(self.main)
        style.theme_use("clam")
        style.configure("Green.TButton",
                        background="green",
                        foreground="white",
                        font=("Helvetica", 12),
                        padding=6)
        style.configure("Green.Horizontal.TProgressbar", 
                        troughcolor="white",
                        background="green",
                        foreground="green",
                        bordercolor="black",
                        text="Progress")
        
    def build_main_window(self):
        # Screen header
        now = datetime.datetime.now()
        day_of_week = now.strftime("%A %d %B")

        header = tk.Label(main, text=day_of_week, font=("Arial", 40), bg="white", fg="green")
        header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=210, pady=5)

        self.construct_checklist()
        self.construct_buttons()

    def construct_checklist(self):

        self.events = get_upcoming_events(self.creds)

        def toggle():
            """
            Function to toggle the state of the checkbox and update the progress bar.
            """
            checked = 0
            unchecked = 0
            total = 0

            for var in self.task_vars:
                if var.get():
                    checked += 1
                else:
                    unchecked += 1
                total += 1

            self.progress["value"] = (checked / total) * 100 if total > 0 else 0

        checklist_frame = tk.Frame(main, width=30, height=20, bg = "white", highlightbackground="green", highlightthickness=1)
        checklist_frame.grid(row=1, column=0, sticky="nsw", padx=50, pady=50, rowspan=2)

        checklist_header = tk.Label(checklist_frame, text="To-Do", font=("Arial", 20), bg="white", fg="green")
        checklist_header.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")


        try:
            with open('checkbox_states.json', 'r') as file:
                states = json.load(file)
        except FileNotFoundError:
            states = {}

        self.task_vars = []

        for id, summary in self.events:
            var = tk.BooleanVar(value=states.get(id, False))  # Use the saved state if it exists, otherwise default to False
            self.task_vars.append(var)
            checkbox = tk.Checkbutton(checklist_frame, text=summary, variable=var, bg="white", fg="black", width=30, justify="left", anchor="w", selectcolor="green", padx=3, command=toggle)
            checkbox.grid(row=len(self.task_vars), column=0, sticky="nsw", padx=30, pady=5)

        self.progress = ttk.Progressbar(self.main, orient="horizontal", length=345, mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress.grid(row=3, column=0, padx=0, pady=0)

        toggle()




    def construct_buttons(self):
        file_exists_flag = file_exists("modules.json")

        task_actions_frame = tk.Frame(self.main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
        task_actions_frame.grid(row=1, column=1, sticky="nsw", padx=10, pady=50)

        task_header = tk.Label(task_actions_frame, text="Task Actions", font=("Arial", 20), bg="white", fg="black")
        task_header.grid(row=0, column=1, padx=10, pady=10)

        add_button = ttk.Button(task_actions_frame, text="Add Task", style="Green.TButton", command=lambda: self.add_task_popup(), state="disabled" if not file_exists_flag else "normal")
        add_button.grid(row=1, column=1, padx=10, pady=10)

        edit_button = ttk.Button(task_actions_frame, text="Edit Task", style="Green.TButton", command=lambda: self.edit_task_popup(self.events))
        edit_button.grid(row=1, column=2, padx=10, pady=10)

        delete_button = ttk.Button(task_actions_frame, text="Delete Task", style="Green.TButton", command=lambda: self.delete_task_popup(self.events))
        delete_button.grid(row=2, column=1, padx=10, pady=10)

        other_action_frame = tk.Frame(main, width=40, height=20, bg = "white", highlightbackground="black", highlightthickness=1)
        other_action_frame.grid(row=2, column=1, sticky="nsw", padx=10, pady=50)

        other_header = tk.Label(other_action_frame, text="Other Actions", font=("Arial", 20), bg="white", fg="black")
        other_header.grid(row=0, column=1, padx=10, pady=10)

        add_assignment_button = ttk.Button(other_action_frame, text="Add Assignment", style="Green.TButton", command=self.add_assignment_popup)
        add_assignment_button.grid(row=1, column=1, padx=10, pady=10)

        add_modules_button = ttk.Button(other_action_frame, text="Add Modules", style="Green.TButton", command=lambda: self.add_modules_popup(add_modules_button, add_button), state="disabled" if file_exists_flag else "normal")
        add_modules_button.grid(row=1, column=2, padx=10, pady=10)

        view_key_button = ttk.Button(other_action_frame, text="View Key", style="Green.TButton", command=self.view_key)
        view_key_button.grid(row=2, column=1, padx=10, pady=10)

    def add_task_popup(self):
        add_popup = tk.Toplevel(self.main)
        add_popup.title("Add Task")
        add_popup.geometry("400x450")
        add_popup.configure(bg="white")
        add_popup.resizable(False, False)

        header = tk.Label(add_popup, text= "Add Task", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

        title_label = tk.Label(add_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
        title_label.place(x=100, y=100, anchor=tk.CENTER)
        title_entry = tk.Entry(add_popup, font=('Arial', 15), bg="white", fg="black")
        title_entry.place(x=250, y=100, anchor=tk.CENTER)

        desc_label = tk.Label(add_popup, text="Description", font=('Arial', 15), bg="white", fg="black")
        desc_label.place(x=100, y=150, anchor=tk.CENTER)
        desc_entry = tk.Entry(add_popup, font=('Arial', 15), bg="white", fg="black")
        desc_entry.place(x=250, y=150, anchor=tk.CENTER)

        dropdown_label = tk.Label(add_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
        dropdown_label.place(x=100, y=200, anchor=tk.CENTER)
        module_var = tk.StringVar(add_popup)
        module_chosen = ttk.Combobox(add_popup, width=19, textvariable=module_var)

        with open('modules.json', 'r') as file:
            modules = json.load(file)
            module_chosen['values'] = (modules['10'], modules['9'], modules['5'])

        module_chosen.place(x=250, y=200, anchor=tk.CENTER)

        date_label = tk.Label(add_popup, text="Date", font=('Arial', 15), bg="white", fg="black")
        date_label.place(x=100, y=250, anchor=tk.CENTER)
        date_chooser = DateEntry(add_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        date_chooser.place(x=250, y=250, anchor=tk.CENTER)

        start_time_label = tk.Label(add_popup, text="Start Time", font=('Arial', 15), bg="white", fg="black")
        start_time_label.place(x=100, y=300, anchor=tk.CENTER)

        start_time_picker = SpinTimePickerModern(add_popup)
        start_time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        start_time_picker.configureAll(bg="white", height=1, fg="black", font=("Arial", 15),
                                clickedcolor="green")
        start_time_picker.configure_separator(bg="white", fg="black")
        start_time_picker.place(x=184, y=300, anchor=tk.CENTER)

        end_time_label = tk.Label(add_popup, text="End Time", font=('Arial', 15), bg="white", fg="black")
        end_time_label.place(x=100, y=350, anchor=tk.CENTER)

        end_time_picker = SpinTimePickerModern(add_popup)
        end_time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        end_time_picker.configureAll(bg="white", height=1, fg="black", font=("Arial", 15),
                                clickedcolor="green")
        end_time_picker.configure_separator(bg="white", fg="black")
        end_time_picker.place(x=184, y=350, anchor=tk.CENTER)

        add_task_button = ttk.Button(add_popup, text="Add", style="Green.TButton", command=lambda: [add_task(self.creds, title_entry.get(), desc_entry.get(), module_var.get(), start_time_picker.hours(), start_time_picker.minutes(), end_time_picker.hours(), end_time_picker.minutes(), date_chooser.get_date()), self.construct_checklist(), add_popup.destroy()])
        add_task_button.place(x=200, y=400, anchor=tk.CENTER)

    def edit_task_popup(self, events):

        def task_to_edit(event):
            task = task_chosen.get()
            task_id = next(x[0] for x in self.events if x[1] == task)
            details = retrieve_event_details(task_id)
            prefill_edit_popup(details)

        edit_popup = tk.Toplevel(self.main)
        edit_popup.title("Edit Task")
        edit_popup.geometry("400x450")
        edit_popup.configure(bg="white")
        edit_popup.resizable(False, False)
        header = tk.Label(edit_popup, text= "Edit Task", font=('Arial', 30), bg="white", fg="Green")
        header.place(x=200, y=30, anchor=tk.CENTER)

        if events == []:
            no_events_label = tk.Label(edit_popup, text="No tasks to edit", font=('Arial', 15), bg="white", fg="black")
            no_events_label.place(x=200, y=100, anchor=tk.CENTER)
        else:
            dropdown_label = tk.Label(edit_popup, text="Task", font=('Arial', 15), bg="white", fg="black")
            dropdown_label.place(x=100, y=100, anchor=tk.CENTER)
            task_var = tk.StringVar(edit_popup)
            task_chosen = ttk.Combobox(edit_popup, width=19, textvariable=task_var)
            task_chosen['values'] = [x[1] for x in self.events]
            task_chosen.place(x=250, y=100, anchor=tk.CENTER)
            task_chosen.bind("<<ComboboxSelected>>", task_to_edit)

        def prefill_edit_popup(details):
            # Autofill fields with selected task details

            title_label = tk.Label(edit_popup, text="Title", font=('Arial', 15), bg="white", fg="black")
            title_label.place(x=100, y=150, anchor=tk.CENTER)
            title_entry = tk.Entry(edit_popup, font=('Arial', 15), bg="white", fg="black")
            title_entry.place(x=250, y=150, anchor=tk.CENTER)

            desc_label = tk.Label(edit_popup, text="Description", font=('Arial', 15), bg="white", fg="black")
            desc_label.place(x=100, y=200, anchor=tk.CENTER)
            desc_entry = tk.Entry(edit_popup, font=('Arial', 15), bg="white", fg="black")
            desc_entry.place(x=250, y=200, anchor=tk.CENTER)

            location_label = tk.Label(edit_popup, text="Location", font=('Arial', 15), bg="white", fg="black")
            location_label.place(x=100, y=250, anchor=tk.CENTER)
            location_entry = tk.Entry(edit_popup, font=('Arial', 15), bg="white", fg="black")
            location_entry.place(x=250, y=250, anchor=tk.CENTER)

            dropdown_label = tk.Label(edit_popup, text="Module", font=('Arial', 15), bg="white", fg="black")
            dropdown_label.place(x=100, y=300, anchor=tk.CENTER)
            module_var = tk.StringVar(edit_popup)
            module_chosen = ttk.Combobox(edit_popup, width=19, textvariable=module_var)

            with open('modules.json', 'r') as file:
                modules = json.load(file)
                module_chosen['values'] = (modules['10'], modules['9'], modules['5'])

            module_chosen.place(x=250, y=300, anchor=tk.CENTER)

            date_label = tk.Label(edit_popup, text="Date", font=('Arial', 15), bg="white", fg="black")
            date_label.place(x=100, y=350, anchor=tk.CENTER)
            date_chooser = DateEntry(edit_popup, width=19, background='green', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
            date_chooser.place(x=250, y=350, anchor=tk.CENTER)

            edit_task_button = ttk.Button(edit_popup, text="Save", style="Green.TButton", command=lambda: edit_task(self.creds))
            edit_task_button.place(x=200, y=400, anchor=tk.CENTER)


    def delete_task_popup(self, events):
        delete_popup = tk.Toplevel(self.main)
        delete_popup.title("Delete Task")
        delete_popup.geometry("400x200")
        delete_popup.configure(bg="white")
        delete_popup.resizable(False, False)
        header = tk.Label(delete_popup, text= "Delete Task", font=('Arial', 30), bg="white", fg="Green")
        header.place(x=200, y=30, anchor=tk.CENTER)

        if events == []:
            no_events_label = tk.Label(delete_popup, text="No tasks to delete", font=('Arial', 15), bg="white", fg="black")
            no_events_label.place(x=200, y=100, anchor=tk.CENTER)
        else:
            dropdown_label = tk.Label(delete_popup, text="Task", font=('Arial', 15), bg="white", fg="black")
            dropdown_label.place(x=100, y=100, anchor=tk.CENTER)
            task_var = tk.StringVar(delete_popup)
            task_chosen = ttk.Combobox(delete_popup, width=19, textvariable=task_var)
            task_chosen['values'] = events
            task_chosen.place(x=250, y=100, anchor=tk.CENTER)

            delete_task_button = ttk.Button(delete_popup, text="Delete", style="Green.TButton", command=lambda: delete_task(self.creds))
            delete_task_button.place(x=200, y=170, anchor=tk.CENTER)

    def add_assignment_popup(self):
        add_assignment_popup = tk.Toplevel(self.main)
        add_assignment_popup.title("Add Assignment")
        add_assignment_popup.geometry("400x400")
        add_assignment_popup.configure(bg="white")
        add_assignment_popup.resizable(False, False)
        header = tk.Label(add_assignment_popup, text= "Add Assignment", font=('Arial', 30), bg="white", fg="Green")
        header.place(x=200, y=30, anchor=tk.CENTER)

    def view_key(self):
        key_popup = tk.Toplevel(self.main)
        key_popup.title("View Key")
        key_popup.geometry("400x400")
        key_popup.configure(bg="white")
        key_popup.resizable(False, False)
        header = tk.Label(key_popup, text= "Key", font=('Arial', 30), bg="white", fg="Green")
        header.place(x=200, y=30, anchor=tk.CENTER)

        modules_frame = tk.Frame(key_popup, width=30, height=20, bg = "white", highlightbackground="green", highlightthickness=1)
        modules_frame.place(x=200, y=220, anchor=tk.CENTER)

        i = 0

        if file_exists("modules.json"):
            with open('modules.json', 'r') as file:
                modules_data = json.load(file)
                for module in modules_data.values():
                    module_label = tk.Label(modules_frame, text=module, font=('Arial', 15), bg="white", fg="black")
                    module_label.grid(row=i, column=0, padx=30, pady=20)
                    i += 1
        else:
            no_modules_label = tk.Label(modules_frame, text="No modules added", font=('Arial', 15), bg="white", fg="black")
            no_modules_label.grid(row=i, column=0, padx=30, pady=20)

        canvas = tk.Canvas(modules_frame, width=70, height=200, bg="white", highlightbackground="white", highlightthickness=1)
        canvas.grid(row=0, column=1, padx=20, pady=20, rowspan=3)
        

        # Draw ovals at different Y positions within the canvas
        canvas.create_oval(10, 10, 30, 30, fill="green", outline="green")   # top
        canvas.create_oval(10, 90, 30, 110, fill="blue", outline="blue")     # middle
        canvas.create_oval(10, 170, 30, 190, fill="yellow", outline="yellow")# bottom



    def add_modules_popup(self, button_to_disable, button_to_enable):

        modules_popup = tk.Toplevel(self.main)
        modules_popup.title("Add Modules")
        modules_popup.geometry("400x350")
        modules_popup.configure(bg="white")
        modules_popup.resizable(False, False)

        header = tk.Label(modules_popup, text= "Add Modules", font=('Arial', 30), bg="white", fg="Green")
        header.grid(row=0, column=0, padx=120, pady=10)

        module_1_label = tk.Label(modules_popup, text="Module 1", font=('Arial', 15), bg="white", fg="black")
        module_1_label.place(x=100, y=110, anchor=tk.CENTER)
        module_1_entry = tk.Entry(modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_1_entry.place(x=250, y=110, anchor=tk.CENTER)

        module_2_label = tk.Label(modules_popup, text="Module 2", font=('Arial', 15), bg="white", fg="black")
        module_2_label.place(x=100, y=170, anchor=tk.CENTER)
        module_2_entry = tk.Entry(modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_2_entry.place(x=250, y=170, anchor=tk.CENTER)

        module_3_label = tk.Label(modules_popup, text="Module 3", font=('Arial', 15), bg="white", fg="black")
        module_3_label.place(x=100, y=230, anchor=tk.CENTER)
        module_3_entry = tk.Entry(modules_popup, font=('Arial', 15), bg="white", fg="black")
        module_3_entry.place(x=250, y=230, anchor=tk.CENTER)

        def save_modules():
            add_modules(module_1_entry.get(), module_2_entry.get(), module_3_entry.get())
            self.refresh_main_window()
            modules_popup.destroy()
            button_to_disable.config(state="disabled")
            button_to_enable.config(state="normal")

        add_modules_button = ttk.Button(modules_popup, text="Save", style="Green.TButton", command=save_modules)
        add_modules_button.place(x=200, y=300, anchor=tk.CENTER)

    def saved_states(self):
        """
        Function to save the state of the main window when it is closed.
        """
        # with open('checkbox_states.json', 'w') as file:
        #     states = {summary : var.get() for summary, var in zip(self.events, self.task_vars)} # Pairs the summary with the variable, allowing to iterate through the lists simultaneously.
        #     json.dump(states, file)

        with open('checkbox_states.json', 'w') as file:
            states = {id : var.get() for id, var in zip([x[0] for x in self.events], self.task_vars)} # Pairs the summary with the variable, allowing to iterate through the lists simultaneously.
            json.dump(states, file)

    def on_close(self):
        """
        Function to handle the close event of the main window.
        """
        self.saved_states()
        main.destroy()

if __name__ == '__main__':
    main = tk.Tk()
    app = StudentPlannerApp(main)
    main.protocol("WM_DELETE_WINDOW", app.on_close)  # Set the close event handler
    main.mainloop()


# {"Hiya": true, "Hi": false, "Hey": false}
