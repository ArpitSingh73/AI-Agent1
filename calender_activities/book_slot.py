"""
module to book the slot.
"""

def create_event(service, event):
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s \n\n\n" % (created_event.get("htmlLink")))
