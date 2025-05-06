import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_upcoming_events(creds, max_results=10):
    """
    Fetches the next 10 upcoming events from the user's primary Google Calendar.
    """
    try:
        service = build("calendar", "v3", credentials=creds) # Initialise the Calendar API, connects to calendar service using credentials.

        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat() # Gets current time in UTC format, converting it to a strning that Google Caldendar understands.
        print("Getting the upcoming 10 events")
        events_result = ( # Main API request to get the next 10 events.
         service.events()
            .list(
                calendarId="primary", # accesses the user's primary calendar.
                timeMin=now, # Only return events that start after the current time.
                maxResults=10, 
                singleEvents=True, # Returns only single events, not recurring events.
                orderBy="startTime",
            )
            .execute() # Executes the API request, returing the results in a dictionary.
        )
        events = events_result.get("items", []) # Gets the list of events from the API response.

        if not events:
            print("No upcoming events found.")
            return []

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
    # Save modules to a json file
    pass