import requests
import json
from datetime import datetime

def get_id():
    with open("id.txt", "r") as file:
        return file.read()

def cleanse_hour(hour):
    split_hour = hour.split(":", 1)
    return (split_hour[0] if (len(split_hour[0]) == 2) else "0" + split_hour[0]) + split_hour[1]

def get_shift(schedule_day):
    shift = schedule_day["DailyShift"][0]
    if (shift == "-"):
        return 

    date_obj = datetime.strptime(schedule_day["StartDate"], "%Y-%m-%dT%H:%M:%S")

    split_shift = shift.split("-", 1)
    time = datetime.strptime(split_shift[0], "%H:%M")
    start_time_obj = date_obj.replace(hour = time.hour, minute = time.minute)

    split_shift = split_shift[1].split(" ", 1)
    time = datetime.strptime(split_shift[0], "%H:%M")
    end_time_obj = date_obj.replace(hour = time.hour, minute = time.minute)

    dept = split_shift[1]
    
    return (start_time_obj.strftime("%Y%m%dT%H%M%S"), end_time_obj.strftime("%Y%m%dT%H%M%S"), dept)

sess = requests.Session()

employee_id = get_id()

sess.get("https://myschedule.metro.ca/api/Login/" + employee_id)
total_schedule = sess.get("https://myschedule.metro.ca/api/Employee/" + employee_id).json()

with open("calendar.ics", "w") as file:
    file.write("BEGIN:VCALENDAR\n")
    file.write("VERSION:2.0\n")
    file.write("PRODID:SuperNovaa41\n")

for i in range(-1, -8, -1):
    res = get_shift(total_schedule["WorkTime"][i])
    if (res is None):
        continue

    with open("calendar.ics", "a") as file:
        file.write("BEGIN:VEVENT\n")
        file.write("DTSTART:" + res[0] + "\n")
        file.write("DTEND:" + res[1] + "\n")
        file.write("SUMMARY: Work (" + res[2] + ")\n")
        file.write("END:VEVENT\n")

with open("calendar.ics", "a") as file:
    file.write("END:VCALENDAR\n")

