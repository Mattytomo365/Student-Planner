import datetime
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
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat() # Gets current time in UTC format, converting it to a strning that Google Caldendar understands.
        tomorrow = (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)).isoformat() # Gets the time for tomorrow in UTC format.
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
            # start = event["start"].get("dateTime", event["start"].get("date"))
            results.append((event["summary"]))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def add_task(creds):
    pass

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