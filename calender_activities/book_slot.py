"""
module to book the slot.
"""

def create_event(service, event):
    try:
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print("Luna: Event created: %s" % (created_event.get("htmlLink")))
    except Exception as e:
        print("Error while booking the specified event: ", e)    
