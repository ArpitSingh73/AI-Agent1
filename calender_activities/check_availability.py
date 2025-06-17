"""
module to check if a slot is free or not?
"""
from calender_activities.book_slot import create_event

def check_slot_and_book(service, start_time, end_time):
    try:
        print("Luna: Checking if slot is free or not?")
        body = {"timeMin": start_time, "timeMax": end_time, "items": [{"id": "primary"}]}
        events_result = service.freebusy().query(body=body).execute()
        busy_times = events_result["calendars"]["primary"]["busy"]
        if len(busy_times) == 0:  # True if free
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
            return True
    except Exception as e:
        return False        

