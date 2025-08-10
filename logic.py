import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import shutil
import sys


# Get the directory where the executable is running
if getattr(sys, 'frozen', False):
    # Running as a bundled app
    base_dir = sys._MEIPASS
else:
    # Running as script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to bundled (read-only) json files
bundled_checkbox__path = os.path.join(base_dir, 'checkbox_states.json')
bundled_reminder__path = os.path.join(base_dir, 'reminder.json')
bundled_credentials_path = os.path.join(base_dir, 'credentials.json')

# Path to working (writable) json files in App Data
if getattr(sys, 'frozen', False):
    if os.name == "nt":
        working_dir = os.path.join(os.getenv('APPDATA'), 'StudentPlanner')
    elif os.name == "posix":
        working_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'StudentPlanner')
        
    os.makedirs(working_dir, exist_ok=True)
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))

working_checkbox_path = os.path.join(working_dir, 'checkbox_states.json')
working_reminder_path = os.path.join(working_dir, 'reminder.json')
working_modules_path = os.path.join(working_dir, 'modules.json')
working_token_path = os.path.join(working_dir, 'token.json')

# If working jsons doesn't exist, copy from bundled json files
if not os.path.exists(working_checkbox_path):
    shutil.copyfile(bundled_checkbox__path, working_checkbox_path)

if not os.path.exists(working_reminder_path):
    shutil.copyfile(bundled_reminder__path, working_reminder_path)


def file_exists(path):
    """
    Checks if a file exists at the given path.
    """
    is_exists = os.path.exists(path)
    if is_exists:
        return True
    else:
        return False

def get_upcoming_events(creds):
    """
    Fetches upcoming events from the user's primary Google Calendar.
    """
    try:
        service = build("calendar", "v3", credentials=creds) # Initialise the Calendar API, connects to calendar service using credentials.

        # Call the Calendar API
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        tomorrow = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat() # Gets the time for tomorrow in UTC format.
        print("Getting the upcoming 10 events")
        events_result = ( # Main API request to get the next 10 events.
         service.events()
            .list(
                calendarId="primary", # accesses the user's primary calendar.
                timeMin=now, # Only return events that start today.
                q="task", # Only returns tasks and not assignments
                timeMax=tomorrow, # Only return events that start before the next day.
                singleEvents=True, # Returns only single events, not recurring events.
                orderBy="startTime",
            )
            .execute() # Executes the API request, returing the results in a dictionary.
        )
        events = events_result.get("items", []) # Gets the list of events from the API response.

        if not events:
            return [(None, "No tasks today", None)]

     # Returns the start and name of the next 10 events
        results = []
        for event in events:
            results.append((event["id"], event["summary"], event["colorId"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
    
def get_assignments(creds, upcoming):
    """
    Fetches upcoming assignments from the user's primary Google Calendar.
    """
    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        tomorrow = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat()
        if upcoming == True:  # Retrieves assignments due on the current day
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    q="assignment",
                    timeMax=tomorrow,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
        else: # Retrieves all assignments
            events_result = (
            service.events()
                .list(
                    calendarId="primary", 
                    q="assignment", # Only returns assignments and not tasks
                    maxResults=10, 
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

        if not events:
            return [(None, "No assignments", None)]

        results = []
        for event in events:
            results.append((event["id"], event["summary"], event["colorId"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def get_event_by_date(creds, specified_date):
    try:
        service = build("calendar", "v3", credentials=creds)

        specified_date = datetime.datetime(specified_date.year, specified_date.month, specified_date.day)

        specified_day = specified_date.replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        day_after = ((specified_date.replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat() # Gets the time for tomorrow in UTC format.
        events_result = (
         service.events()
            .list(
                calendarId="primary",
                timeMin=specified_day, 
                timeMax=day_after, 
                singleEvents=True, 
                orderBy="startTime",
            )
            .execute() 
        )
        events = events_result.get("items", [])

        if not events:
            return [("no_event_id", "No tasks/assignments to delete")]

        results = []
        for event in events:
            results.append((event["id"], event["summary"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
    
def retrieve_event_details(creds, task_id):
    try:
        """
        Retrieves the details of a specific event using its ID.
        """
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        event = service.events().get(calendarId="primary", eventId=task_id).execute()  # Fetches the event details using the event ID.
        
        return {
            "id": event["id"],
            "summary": event["summary"],
            "colorId": event["colorId"],
            "date": event["start"].get("date", event["start"].get("date")),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date"))
        }
    except HttpError as error:
        print(f"An error occurred while retrieving event details: {error}")
        return []

def retrieve_assignment_details(creds, assignment_id):
    try:
        """
        Retrieves the details of a specific assignment using its ID.
        """
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        event = service.events().get(calendarId="primary", eventId=assignment_id).execute()  # Fetches the event details using the event ID.
        
        return {
            "id": event["id"],
            "summary": event["summary"],
            "colorId": event["colorId"],
            "date": event["start"].get("date", event["start"].get("date")),
            "start": event["start"].get("dateTime", event["start"].get("date")),
        }
    except HttpError as error:
        print(f"An error occurred while retrieving event details: {error}")
        return []
    


def add_task(creds, title, module, start_time, end_time, date):

    try:
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        with open (working_modules_path, "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6
            elif modules['8'] == module:
                colour = 8

        event = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{start_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{end_time[:5]}:00",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().insert(calendarId="primary", body=event).execute()  # Inserts the event into the user's primary calendar.

def edit_task(creds, task_id, title, module, start_time, end_time, date):
    try:
        service = build("calendar", "v3", credentials=creds)

        with open (working_modules_path, "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6
            elif modules['8'] == module:
                colour = 8

        event = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{start_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{end_time[:5]}:00",
                "timeZone": "Europe/London",
            }
        }
    
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    event = service.events().patch(calendarId="primary", eventId=task_id, body=event).execute() # sendNotifications=False ??

def delete_task(creds, task_id):
    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId="primary", eventId=task_id).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

def add_assignment(creds, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        with open (working_modules_path, "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6
            elif modules['8'] == module:
                colour = 8

        event = {
            "summary": f"{title}",
            "description": "assignment", # Differentiating assingment events from regular events in the caldendar
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{due_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{due_time[:5]}:01",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().insert(calendarId="primary", body=event).execute()

def edit_assignment(creds, assignment_id, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        with open (working_modules_path, "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6
            elif modules['8'] == module:
                colour = 8

        event = {
            "summary": f"{title}",
            "description": "assignment",
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{due_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{due_time[:5]}:01",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().patch(calendarId="primary", eventId=assignment_id, body=event).execute()


def add_modules(module_1, module_2, module_3):
    """"
    Adds the modules to a JSON file.
    """
    dictionary = {
        "10" : f"{module_1}",
        "9" : f"{module_2}",
        "6" : f"{module_3}",
        "8" : "General"
    }

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    with open(working_modules_path, "w") as outfile:
        outfile.write(json_object)

def save_reminder_state(reminded, date):
    dictionary ={
        "reminded": f"{reminded}",
        "date": f"{date}"
    }

    json_object = json.dumps(dictionary, indent=4)

    with open(working_reminder_path, "w") as outfile:
        outfile.write(json_object)


