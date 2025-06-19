# import datetime

# now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
# print(now)

from datetime import datetime
from zoneinfo import ZoneInfo

# Get current time in UTC
now_utc = datetime.now(tz=ZoneInfo("UTC"))

# Convert to IST timezone
now_ist = now_utc.astimezone(ZoneInfo("Asia/Kolkata"))

# Get ISO format string
now_ist_str = now_ist.isoformat()
print(now_ist_str)
