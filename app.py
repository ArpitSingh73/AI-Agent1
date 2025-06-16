import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from calender_activities.book_slot import create_event
from calender_activities.check_availability import is_slot_free
from llm_activities.user_bot_conversation import extract_date_time

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
from random import randint


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
        # now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
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
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])

        response = extract_date_time(chat_history, now)
 
        if "insufficient_context" in response["response"]:
            return {"success": False, "response": "insufficient context"}

        start_time = response["response"]["start_time"]
        end_time = response["response"]["end_time"]

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
            return {"success": True, "response": "event created"}
        else:
            print("OOps, Time slot is busy!")
            return {"success": False, "response": "slot occupied"}

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    chat_history = [
        # "how are you?",
        # "I need to meet for 45 minutes sometime before my flight that leaves on Friday at 6 PM",
        # "have some plans for today.",
        # "need to check fot some other day.",
    ]

    insuffficient_context_replies = [
        "Can you please let me know about the date and time you want to schedule the call?",
        "Please enter the timing details of the meet.",
        "Kindly share the time information you are free to schedule the call.",
        "Please share the time and date you want me to book the call",
    ]

    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    user_input = input(
        "Luna: Hi, I'm Luna. I am here to help you to schedule your next meeting. Please enter 'exit' to stop the conversation! \nUser: "
    )

    while True:
        if user_input == "exit":
            break
        print("User input: ", user_input)
        chat_history.append("User : " + user_input)
        response = main(chat_history, now)
        if response["response"] == "insufficient context":
            user_input = input(
                "Luna: " + insuffficient_context_replies[randint(0, 3)] + "\nUser: "
            )
            chat_history.append("Bot: " + insuffficient_context_replies[randint(0, 4)])
        elif response["response"] == "slot occupied":
            user_input = input(
                "Luna: Hey, you already have this slot occupied, lets choose some other one.\nUser: "
            )
            chat_history.append(
                "Bot: Hey, you already have this slot occupied, lets choose some other one."
            )
        elif response["response"] == "event created":
            print(
                "Luna: Hey, call has been scheduled, please check your email."
            )
            break
