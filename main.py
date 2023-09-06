import os
import utils
import datetime


DAYS_TO_FETCH = int(os.environ.get('DAYS_TO_FETCH', 31))
LAST_DATE = ""
if os.path.exists('last_date'):
    with open('last_date', 'r') as f:
        LAST_DATE = f.read().strip()

if not LAST_DATE:
    LAST_DATE = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

days = 0
while days <= DAYS_TO_FETCH:
    date = utils.next_day(LAST_DATE)
    LAST_DATE = date
    days += 1
    print(f"Fetching {date}")
    timetable = utils.get_timetable(date)
    for lesson in timetable:
        print(f"Adding {lesson['subject_name']} {lesson['room_name']} {lesson['start_time']} {lesson['end_time']} {lesson['teacher_name']}")
        teacher_initials = lesson['teacher_name'].split(' ')[1][0] + lesson['teacher_name'].split(' ')[-1][0]
        title = f"{lesson['subject_name']} ({teacher_initials})"
        description = f"{lesson['lesson_name']} {lesson['period_name']} ({lesson['lesson_id']})"
        utils.add_event(title, lesson['room_name'], description, lesson['start_time'], lesson['end_time'])


with open('last_date', 'w') as f:
    f.write(LAST_DATE)
