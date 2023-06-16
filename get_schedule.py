import requests
import json

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

    datestr = schedule_day["StartDate"]
    date = datestr[0:4] + datestr[5:7] + datestr[8:10] + "T"

    split_shift = shift.split("-", 1)
    startdate = date + cleanse_hour(split_shift[0]) + "00"

    split_shift = split_shift[1].split(" ", 1)
    enddate = date + cleanse_hour(split_shift[0]) + "00"

    dept = split_shift[1]
    
    return (startdate, enddate, dept)

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

