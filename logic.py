import datetime
from datetime import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

def get_upcoming_events(creds):
    """
    Fetches the next 10 upcoming events from the user's primary Google Calendar.
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
                timeMax=tomorrow, # Only return events that start before the next day.
                maxResults=10, 
                singleEvents=True, # Returns only single events, not recurring events.
                orderBy="startTime",
            )
            .execute() # Executes the API request, returing the results in a dictionary.
        )
        events = events_result.get("items", []) # Gets the list of events from the API response.

        if not events:
            return ["No events today"]

     # Returns the start and name of the next 10 events
        results = []
        for event in events:
            results.append((event["id"], event["summary"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
    
def retrieve_event_id(creds, summary):
    try:
        service = build("calendar", "v3", credentials=creds)
        events_result = ( # Main API request to get the next 10 events.
         service.events()
            .list(
                summary = f"{summary}" # accesses the user's primary calendar.
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            return ["Event not found"]

        for event in events:
            result = (event["id"])
        
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def add_task(creds, title, desc, module, start_time_hour, start_time_minute, end_time_hour, end_time_minute, date):

    try:
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        with open ("modules.json", "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['5'] == module:
                colour = 5
                
        print(date)
        print(start_time_hour)
        print(start_time_minute)
        print(end_time_hour)
        print(end_time_minute)

        # CAN I REMOVE LOCATION, RECURRENCE AND ATTENDEES?
        # Allow for the user to view the description they added?

        event = {
            "summary": f"{title}",
            "location": "Somewhere", # Remove
            "description": f"{desc}",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{start_time_hour}:{start_time_minute}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{end_time_hour}:{end_time_minute}:00",
                "timeZone": "Europe/London",
            },
            "recurrence": [ # Remove
                "RRULE:FREQ=DAILY;COUNT=1"  # Sets the event to recur daily for one occurrence.
            ],
            "attendees": [ # Remove
                {"email": "matty.tom@outlook.com"}
            ]
        }

    except HttpError as error:
        print(f"An error occurred: {error}")
        
    event = service.events().insert(calendarId="primary", body=event).execute()  # Inserts the event into the user's primary calendar.

def edit_task(creds):
    pass

def delete_task(creds):
    pass

def add_assignment(creds):
    pass

def view_key():
    pass

def add_modules(module_1, module_2, module_3):
    """"
    Adds the modules to a JSON file.
    """
    dictionary = {
        "10" : f"{module_1}",
        "9" : f"{module_2}",
        "5" : f"{module_3}"
    }

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open("modules.json", "w") as outfile:
        outfile.write(json_object)

def file_exists(path):
    """
    Checks if a file exists at the given path.
    """
    is_exists = os.path.exists(path)
    if is_exists:
        return True
    else:
        return False
    
def get_task_details(task):
    """
    Returns the task details.
    """
    pass
