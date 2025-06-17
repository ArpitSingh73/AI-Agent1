"""
module to fetch calender events if any
"""

def fetch_calender_events(service, now):

    try:
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
        upcoming_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            upcoming_events.append(str(event["summary"]))
            # print(start, end , event["summary"])
            event_info = {
                "start_time": start,
                "end_time": end,
                "event": event["summary"],
            }
            upcoming_events.append(event_info)
            return upcoming_events
    except Exception as e:
        print(e) 
        return []       