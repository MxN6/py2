from datetime import datetime, timedelta
import sys

def parse_line(line):
    date_part, tz_part = line.split()

    # Parse date (local midnight)
    dt = datetime.strptime(date_part, "%Y-%m-%d")

    # Parse timezone
    sign = 1 if '+' in tz_part else -1
    hh, mm = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hh, minutes=mm)

    # Convert local midnight to UTC
    return dt - sign * offset


line1 = input().strip()
line2 = input().strip()

utc1 = parse_line(line1)
utc2 = parse_line(line2)

diff_seconds = abs((utc1 - utc2).total_seconds())
print(int(diff_seconds // 86400))