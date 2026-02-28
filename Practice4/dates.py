from datetime import datetime, timedelta, timezone

# -----------------------
# 1. Creating Date Objects
# -----------------------

now = datetime.now()
print("Current Date and Time:", now)

specific_date = datetime(2025, 1, 1)
print("Specific Date:", specific_date)


# -----------------------
# 2. Date Formatting
# -----------------------

formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted Date:", formatted)


# -----------------------
# 3. Time Difference
# -----------------------

future_date = now + timedelta(days=10)
difference = future_date - now
print("Difference in days:", difference.days)


# -----------------------
# 4. Working with Timezones
# -----------------------

utc_now = datetime.now(timezone.utc)
print("UTC Time:", utc_now)

offset = timezone(timedelta(hours=6))  # UTC+6 (e.g. Kazakhstan)
local_time = utc_now.astimezone(offset)
print("UTC+6 Time:", local_time)