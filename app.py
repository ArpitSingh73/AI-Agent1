import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from calender_activities.book_slot import create_event
from calender_activities.check_availability import is_slot_free
from llm_activities.user_bot_conversation import extract_date_time

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main(chat_history, now):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # if not events:
        #     print("No upcoming events found.")
        #     return

        # # Prints the start and name of the next 10 events
        upcoming_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            upcoming_events.append(str(event["summary"]))
            print(start, event["summary"])

        response = extract_date_time(chat_history, now, upcoming_events)["response"]

        if "insufficient_context" in response:
            return {
                "type": "insufficient_context",
                "message": response["insufficient_context"],
            }
        elif "greeting" in response:
            return {
                "type": "greeting",
                "message": response["greeting"],
            }
        elif "invalid_query" in response:
            return {
                "type": "invalid_query",
                "message": "OOps the query is out of the context for me. Kindly ask something relevant.",
            }
        elif "llm_failure" in response:
            return {
                "type": "llm_failure",
                "message": "something went wrong!",
            }

        start_time = response["start_time"]
        end_time = response["end_time"]

        # start_time = '2025-06-20T14:00:00+05:30'
        # end_time = '2025-06-20T15:00:00+05:30'

        if is_slot_free(service, start_time, end_time):
            print("Time slot is free!")
            event = {
                "summary": "Team Meeting",
                "location": "Conference Room",
                "description": "Discuss project updates.",
                "start": {
                    "dateTime": start_time,
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": "Asia/Kolkata",
                },
                "attendees": [
                    {"email": "arpitsingh73073@gmail.com"},
                    {"email": "arpit21116@recmainpuri.in"},
                ],
                "reminders": {
                    "useDefault": True,
                },
            }

            create_event(service, event)
            return {"type": "event_created", 
                    "message" : "Wow, call has been scheduled successfully, please check your inbox."}
        else:
            print("OOps, Time slot is busy!")
            return {
                "type": "slot_occupied",
                "message": "Luna: Hey, you already have this slot occupied, lets choose some other one.\nUser: "
            }

    except Exception as error:
        return {"message": "something went wrong!"}
        # print(f"An error occurred: {error}")


if __name__ == "__main__":
    
    chat_history = []
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    user_input = input(
        "Luna: Hi, I'm Luna. I am here to help you to schedule your next meeting. Please enter 'exit' to stop the conversation! \nUser: "
    )

    while True:
        if user_input == "exit":
            break
        chat_history.append("User : " + user_input)
        response = main(chat_history, now)

        if response["type"] == "event_created":
            print("Luna: Hey, call has been scheduled, please check your email.")
            break
        elif response["message"] == "llm_failure":
            print("Something went wrong, lets try again!")
            break
        else:
                user_input = input(
                    "Luna: " + response["message"]+ "\nUser: "
                )
                chat_history.append("Bot: " + response["message"])
