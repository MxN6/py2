from datetime import datetime, timedelta


def parse(line):
    date_part, time_part, tz_part = line.split()

    dt = datetime.strptime(date_part + " " + time_part,
                           "%Y-%m-%d %H:%M:%S")

    sign = 1 if '+' in tz_part else -1
    hh, mm = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hh, minutes=mm)

    # Convert local time to UTC
    return dt - sign * offset


start_line = input().strip()
end_line = input().strip()

start_utc = parse(start_line)
end_utc = parse(end_line)

duration = int((end_utc - start_utc).total_seconds())

print(duration)