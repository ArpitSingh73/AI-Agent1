"""
main file of the app.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from calender_activities.fetch_events import fetch_calender_events
from calender_activities.check_availability import check_slot_and_book
from agent_activities.user_llm_conversation import extract_date_time
from agent_activities.analyze_agent_response import analyze_agent_response
from text_speech_activities.text_to_speech import convert_text_to_speech
from text_speech_activities.take_user_input import listen_to_user
from agent_activities.save_chat_history import save_context

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main(chat_history, now):
    """
    Main function to handle user query.
    """
    creds = None

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

        service = build(
            "calendar", "v3", credentials=creds
        )  # create a calender service
        upcoming_events = fetch_calender_events(
            service, now
        )  # call calender API to cheeck for events
        response = extract_date_time(chat_history, now, upcoming_events)[
            "response"
        ]  # use agentic logic to extract date and time
        response = analyze_agent_response(
            response
        )  # take actions according to agent Luna

        if "type" in response:  # agent needs more details to schedule a call
            return response

        start_time = response["start_time"]
        end_time = response["end_time"]

        convert_text_to_speech("let me check the availability of specified slot.")

        if check_slot_and_book(
            service, start_time, end_time
        ):  # if slot is empty, book it else inform the user
            convert_text_to_speech("Time slot is free! Give me a moment to book it.")

            return {
                "type": "event_created",
                "message": "Wow, call has been scheduled successfully, please check your inbox.",
            }
        else:
            convert_text_to_speech(
                "The specified slot os already occupied, lets try other options."
            )
            print(
                "Luna: The specified slot os already occupied, lets try other options."
            )

            return {
                "type": "slot_occupied",
                "message": "Luna: Hey, you already have this slot occupied, lets choose some other one. ",
            }

    except Exception as error:
        print(error)
        return {"type": "llm_failure", "message": "something went wrong!"}


if __name__ == "__main__":

    # Check if file exists
    filename = "context.json"
    chat_history = []

    if os.path.isfile(filename):
        # Read existing data
        with open(filename, "r") as file:
            try:
                chat_history = json.load(file)
            except json.JSONDecodeError:
                chat_history = []
    else:
        chat_history = []

    # Get current time in UTC
    now_utc = datetime.now(tz=ZoneInfo("UTC"))
    # Convert to IST timezone
    now_ist = now_utc.astimezone(ZoneInfo("Asia/Kolkata"))
    # Get ISO format string
    now = now_ist.isoformat() 
    main([], now)
    # now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    convert_text_to_speech("Hi I am luna, how can I assist you today?")
    print("Luna: Hi I am luna, how can I assist you today?")

    while True:
        user_input = listen_to_user()
        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        chat_history.append("User : " + user_input)
        save_context("User : " + user_input)
        response = main(chat_history, now)

        if response["type"] == "event_created":
            convert_text_to_speech(
                "Hey, call has been scheduled, please check your email."
            )
            print("Luna: Hey, call has been scheduled, please check your email.")
            os.remove(filename)  # delete the context
            break
        elif response["message"] == "llm_failure":
            convert_text_to_speech("Something went wrong, lets try again!")
            print("Luna: Something went wrong, lets try again!")
            break
        else:
            user_input = listen_to_user()
            chat_history.append("Bot: " + response["message"])
            save_context("Bot: " + response["message"])
            convert_text_to_speech(response["message"])
            print("Luna: " + response["message"])
