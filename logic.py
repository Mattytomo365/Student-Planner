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
            return [(None, "No events today", None)]

     # Returns the start and name of the next 10 events
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
            return [("no_event_id", "No tasks to delete")]

        results = []
        for event in events:
            results.append((event["id"], event["summary"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
    
def retrieve_event_details(creds, id):
    try:
        """
        Retrieves the details of a specific event using its ID.
        """
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        event = service.events().get(calendarId="primary", eventId=id).execute()  # Fetches the event details using the event ID.
        
        return {
            "id": event["id"],
            "summary": event["summary"],
            "description": event["description"],
            "location": event["location"],
            "colorId": event["colorId"],
            "date": event["start"].get("date", event["start"].get("date")),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date"))
        }
    except HttpError as error:
        print(f"An error occurred while retrieving event details: {error}")
        return []
    


def add_task(creds, title, desc, module, start_time, end_time, date):

    try:
        service = build("calendar", "v3", credentials=creds)  # Initialize the Calendar API
        with open ("modules.json", "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6

        event = {
            "summary": f"{title}",
            "description": f"{desc}",
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

def edit_task(creds, task_id, title, desc, module, start_time, end_time, date):
    try:
        service = build("calendar", "v3", credentials=creds)

        with open ("modules.json", "r") as f:
            modules = json.load(f)
            if modules['10'] == module:
                colour = 10
            elif modules['9'] == module:
                colour = 9
            elif modules['6'] == module:
                colour = 6

        event = {
            "summary": f"{title}",
            "description": f"{desc}",
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
