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
bundled_checkbox_path = os.path.join(base_dir, 'checkbox_states.json')
bundled_reminder_path = os.path.join(base_dir, 'reminder.json')
bundled_modules_path = os.path.join(base_dir, 'modules.json')
bundled_credentials_path = os.path.join(base_dir, 'credentials.json')


# Path to working (writable) json files in App Data
if getattr(sys, 'frozen', False):
    if os.name == "nt":
        working_dir = os.path.join(os.getenv('APPDATA'), 'DesktopPlanner')
    elif os.name == "posix":
        working_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'DesktopPlanner')
        
    os.makedirs(working_dir, exist_ok=True)
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))


working_checkbox_path = os.path.join(working_dir, 'checkbox_states.json')
working_reminder_path = os.path.join(working_dir, 'reminder.json')
working_modules_path = os.path.join(working_dir, 'modules.json')
working_token_path = os.path.join(working_dir, 'token.json')
module_colour_ids = ["10", "9", "6", "11", "5", "4", "3", "2", "1", "7"]
deadline_search_terms = ("deadline", "assign" + "ment")

# If working jsons doesn't exist, copy from bundled json files
if not os.path.exists(working_checkbox_path):
    shutil.copyfile(bundled_checkbox_path, working_checkbox_path)

if not os.path.exists(working_reminder_path):
    shutil.copyfile(bundled_reminder_path, working_reminder_path)

if not os.path.exists(working_modules_path):
    shutil.copyfile(bundled_modules_path, working_modules_path)


def file_exists(path):
    """
    Checks if a file exists at the given path.
    """
    is_exists = os.path.exists(path)
    if is_exists:
        return True
    else:
        return False


def to_24_hour(time_value):
    return datetime.datetime.strptime(time_value, "%I:%M %p").strftime("%H:%M")

def get_colour_for_module(module):
    with open(working_modules_path, "r") as f:
        modules = json.load(f)
    for colour_id, module_name in modules.items():
        if module_name == module:
            return int(colour_id)
    return 8

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
                timeMin=now, # Only return events that start after the current time.
                q="task", # Only returns tasks and not deadlines
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
    
def get_deadlines(creds, upcoming):
    """
    Fetches upcoming deadlines from the user's primary Google Calendar.
    """
    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        tomorrow = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat()
        events = []
        for search_term in deadline_search_terms:
            if upcoming == True:  # Retrieves deadlines due on the current day
                events_result = service.events().list(
                    calendarId="primary",
                    timeMin=now,
                    q=search_term,
                    timeMax=tomorrow,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()
            else: # Retrieves all deadlines
                events_result = service.events().list(
                    calendarId="primary",
                    q=search_term,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()
            events.extend(events_result.get("items", []))

        unique_events = {}
        for event in events:
            unique_events[event["id"]] = event
        events = list(unique_events.values())

        if not events:
            return [(None, "No deadlines", None)]

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
            return [("no_event_id", "No tasks/deadlines to delete")]

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

def retrieve_deadline_details(creds, deadline_id):
    try:
        """
        Retrieves the details of a specific deadline using its ID.
        """
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        event = service.events().get(calendarId="primary", eventId=deadline_id).execute()  # Fetches the event details using the event ID.
        
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
        colour = get_colour_for_module(module)

        event = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{to_24_hour(start_time)}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{to_24_hour(end_time)}:00",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().insert(calendarId="primary", body=event).execute()  # Inserts the event into the user's primary calendar.

def edit_task(creds, task_id, title, module, start_time, end_time, date):
    try:
        service = build("calendar", "v3", credentials=creds)

        colour = get_colour_for_module(module)

        event = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{to_24_hour(start_time)}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{to_24_hour(end_time)}:00",
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

def add_deadline(creds, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        colour = get_colour_for_module(module)

        event = {
            "summary": f"{title}",
            "description": "deadline", # Differentiating deadline events from regular events in the calendar
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{to_24_hour(due_time)}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{to_24_hour(due_time)}:01",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().insert(calendarId="primary", body=event).execute()

def edit_deadline(creds, deadline_id, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        colour = get_colour_for_module(module)

        event = {
            "summary": f"{title}",
            "description": "deadline",
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{to_24_hour(due_time)}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{to_24_hour(due_time)}:01",
                "timeZone": "Europe/London",
            }
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().patch(calendarId="primary", eventId=deadline_id, body=event).execute()


def add_modules(modules):
    """"
    Adds the modules to a JSON file.
    """
    dictionary = {colour_id: module for colour_id, module in zip(module_colour_ids, modules)}
    dictionary["8"] = "General"

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
