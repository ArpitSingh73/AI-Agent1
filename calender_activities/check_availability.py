"""
module to check if a slot is free or not?
"""

def is_time_free(service, start_time, end_time):
    body = {"timeMin": start_time, "timeMax": end_time, "items": [{"id": "primary"}]}
    events_result = service.freebusy().query(body=body).execute()
    busy_times = events_result["calendars"]["primary"]["busy"]
    return len(busy_times) == 0  # True if free
