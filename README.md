# Desktop Planner

---

## Overview

Desktop Planner is a Python & PyQt5 project centred around turning a user's day-to-day tasks into a focused dashboard, syncing tasks & deadlines with the user's Google Calendar.

Tasks can be added, modified, deleted, categorised and checked off through a simple, navigable interface featuring a prominent day-to-day checklist.

The application integrates and syncs with the user's Google Calendar via the Google Calendar API (facilitating OAuth 2.0 through Google Cloud Console) to read/write tasks, keeping schedules in a centralised location.


---

## Features

- **Google Calendar Sync:** Automatically fetches and updates tasks and assignments from your Google Calendar.
- **Day-to-Day Checklist:** Add, edit, categorize, and complete tasks with a simple checklist interface.
- **Module Management:** Assign tasks/assignments to modules, and customize module names.
- **Visual Tagging:** Color-coded modules and visual tags for different categories or modules (terminology controlled by user).
- **Reminders:** Get notified of upcoming deadlines.
- **Progress Tracking:** Visual progress bar for daily task completion.
- **Persistent State:** Saves checkbox states and module settings between sessions.
- **Easy Task Editing:** Edit or delete tasks and deadlines by title.
- **User-Friendly GUI:** Built with PyQt5 dashboards and widgets for simplicity.

---

## Technologies Used

- [Visual Studio Code](https://code.visualstudio.com/): Primary IDE used throughout development.
- [Google Calendar API](https://developers.google.com/workspace/calendar/api/guides/overview): External API used to access the user's google calendar.
- [Python 3.12.7](https://www.python.org/): Primary programming language.
- [PyQt5](https://pypi.org/project/PyQt5/): GUI.

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
- **`Student-Planner2.0`** (merged): Refurbished code for updated Desktop Planner project.

---

## Setup Instructions

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- IDE of your choice

### Installation

#### Option 1 - Packaged Executable:

**Note**: This project will be fully packaged and released for public use when I have fully implemented my personal portfolio website, as Google requires authorised domains for application homepages and privacy policies for verification.

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

4. Run the application:

    ```
    python gui.py
    ```

### Usage

1. **Add Modules**: Click "Add Modules" and enter your module names, adjusting module amount if necessary.
2. **Use Categories** Click "Use Categories" to switch "module" terminology to a more generic "category" terminology
3. **Add/Edit Tasks**: Use the "Add Task" or "Edit Task" buttons to manage your daily tasks.
4. **Add/Edit Assignments**: Use the "Add Assignment" or "Edit Assignment" buttons for academic deadlines.
5. **Checklist**: Check off tasks as you complete them; progress is tracked visually.
6. **Reminders**: The app will notify you of upcoming assignment deadlines.
7. **Delete Tasks/Assignments**: Remove items by date or title using the "Delete" button.

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