from datetime import datetime, timedelta


def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)


def parse(line):
    date_part, tz_part = line.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")

    sign = 1 if '+' in tz_part else -1
    hh, mm = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hh, minutes=mm)

    return dt, sign, offset


birth_line = input().strip()
current_line = input().strip()

birth_dt, birth_sign, birth_offset = parse(birth_line)
current_dt, current_sign, current_offset = parse(current_line)

# Convert current moment to UTC
current_utc = current_dt - current_sign * current_offset

# Express current moment in birth timezone
current_in_birth_tz = current_utc + birth_sign * birth_offset

month = birth_dt.month
day = birth_dt.day

year = current_in_birth_tz.year

# Handle Feb 29
if month == 2 and day == 29 and not is_leap(year):
    day_this = 28
else:
    day_this = day

birthday_local = datetime(year, month, day_this)

# If birthday already passed in birth timezone → next year
if birthday_local < current_in_birth_tz:
    year += 1
    if month == 2 and day == 29 and not is_leap(year):
        day_this = 28
    else:
        day_this = day
    birthday_local = datetime(year, month, day_this)

# Convert chosen birthday to UTC
birthday_utc = birthday_local - birth_sign * birth_offset

# Compute exact second difference
delta_seconds = (birthday_utc - current_utc).total_seconds()

if delta_seconds <= 0:
    print(0)
else:
    print(int(delta_seconds // 86400))  