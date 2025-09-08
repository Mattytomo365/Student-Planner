# Student Planner Application

---

## Overview

Student Planner is a Python & Tkinter project centred around turning a student's day into a focused checklist, syncing tasks & assignments with the user's Google Calendar.

Tasks can be added, modified, deleted, categorised (module specific or general) and checked off through a simple, navigable interface featuring a prominent day-to-day checklist.

The application integrates and syncs with the user's Google Calendar via the Google Calendar API (facilitating OAuth 2.0 through Google Cloud Console) to read/write tasks, keeping schedules in a centralised location.

---

## What I've Learned

An understanding of OAuth 2.0 was required in order to configure this project in the Google Cloud Console. I learnt fundamentals such as scopes and credentials allowing the application to authenticate itself against Google's OAuth servers. Credentials were also utilised to create & manage access tokens, enabling secure access to protected resources on the user's behalf.

Reliable JSON file management was required to manage this project's state across multiple environments (MacOS & Windows). This took the form of a system which copies bundled files from the temporary directory created by Pyinstaller, transferring them into the users working directory, allowing states of the application's components to be accessed and modified when necessary.

---

## Features

- **Google Calendar Sync:** Automatically fetches and updates tasks and assignments from your Google Calendar.
- **Day-to-Day Checklist:** Add, edit, categorize, and complete tasks with a simple checklist interface.
- **Module Management:** Assign tasks/assignments to modules, and customize module names.
- **Visual Tagging:** Color-coded modules and visual tags for different types of days (e.g., rest day, deadline day).
- **Reminders:** Get notified of upcoming deadlines.
- **Progress Tracking:** Visual progress bar for daily task completion.
- **Persistent State:** Saves checkbox states and module settings between sessions.
- **Easy Task Editing:** Edit or delete tasks and assignments by date or title.
- **User-Friendly GUI:** Built with Tkinter and tkcalendar for a modern, responsive interface.

---

## Technologies Used

- [Visual Studio Code](https://code.visualstudio.com/): Primary IDE used throughout development.
- [Google Calendar API](https://developers.google.com/workspace/calendar/api/guides/overview): External API used to access the user's google calendar.
- [Python 3.13.2](https://www.python.org/): Langauge used for GUI and application logic.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): Python library used to build GUI.

---

## Project Structure

### Key Files

- `gui.py`: Main GUI application.
- `logic.py`: Core logic for interacting with Google Calendar and managing data.
- `main.py`: Handles authentication with Google APIs.
- `modules.json`: Stores user-defined module names.
- `checkbox_states.json`: Saves the state of checklist items.
- `reminder.json`: Tracks reminder state for deadlines.
- `credentials.json`: Google API credentials (not included in repo).
- `token.json`: Generated after authentication (not included in repo).
- `requirements.txt`: Python dependencies.

### Branches Overview

- `add-task-feature` (merged): Add task logic.
- `edit-task-feature` (merged): Edit task logic.
- `delete-task/modules-feature` (merged): Delete task/assignment & clear modules logic.
- `assignment-feature` (merged): Add & edit assignment logic.
- `validation-improvements` (merged): Input validation & error handling.

---

## Setup Instructions

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- IDE of your choice

### Installation

#### Option 1 - Packaged Executable:

Download the latest executable file (`.exe`) displayed in the **Releases** tab.

#### Option 2 - Source Code:

1. Clone the repository:

    ```
    git clone https://github.com/Mattytomo365/Student-Planner.git
    ```

2. Navigate to the project directory:

    ```
    cd Student_Planner
    ```

3. Install dependencies (a virtual environment is recommended):

    ```
    python -m venv venv
    .\venv\Scripts\activate (Windows)
    source venv/bin/activate (MacOS)
    pip install -r requirements.txt
    ```

4. Google API Setup:
    - Create a new [Google Cloud Console](https://console.cloud.google.com/) project
    - Enable the Google Calendar API
    - Construct OAuth consent screen
    - Create & download client ID credentials
    - Rename the downloaded file to `credentials.json` & place it in the project root directory  

    For a full walkthrough, follow the [Python Quickstart Guide](https://developers.google.com/workspace/calendar/api/quickstart/python)

4. Run the application:

    ```
    python gui.py
    ```

### Usage

1. **Add Modules**: Click "Add Modules" and enter your module names. This enables task and assignment management.
2. **Add/Edit Tasks**: Use the "Add Task" or "Edit Task" buttons to manage your daily tasks.
3. **Add/Edit Assignments**: Use the "Add Assignment" or "Edit Assignment" buttons for academic deadlines.
4. **Checklist**: Check off tasks as you complete them; progress is tracked visually.
5. **Reminders**: The app will notify you of upcoming assignment deadlines.
6. **Delete Tasks/Assignments**: Remove items by date or title using the "Delete" button.

---

## License

This project is licensed under the MIT license, please see `LICENSE` for details.

---
## Contributing

**Contributions are welcome!**  
Please fork the repository and submit a pull request with your changes.

---

## Contact

For any questions or feedback, feel free to reach out:

- **Email:** matty.tom@icloud.com
- **GitHub:** [Mattytomo365](https://github.com/Mattytomo365)