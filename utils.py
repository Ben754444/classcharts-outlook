import requests
import os
import uuid
CLASSCHARTS_STUDENT_ID = os.environ.get('CLASSCHARTS_STUDENT_ID')
CLASSCHARTS_AUTHORIZATION = os.environ.get('CLASSCHARTS_AUTHORIZATION')
OUTLOOK_COOKIES = os.environ.get('OUTLOOK_COOKIES')
OUTLOOK_CALENDAR_ID = os.environ.get('OUTLOOK_CALENDAR_ID')
OUTLOOK_EMAIL = os.environ.get('OUTLOOK_EMAIL')
if not CLASSCHARTS_STUDENT_ID:
    raise Exception("CLASSCHARTS_STUDENT_ID not set")

if not CLASSCHARTS_AUTHORIZATION:
    raise Exception("CLASSCHARTS_AUTHORIZATION not set")

if not OUTLOOK_CALENDAR_ID:
    raise Exception("OUTLOOK_CALENDAR_ID not set")

if not OUTLOOK_COOKIES:
    raise Exception("OUTLOOK_COOKIES not set")

if not OUTLOOK_EMAIL:
    raise Exception("OUTLOOK_EMAIL not set")

def next_day(date): # not technically correct but cc doesnt care
    year, month, day = date.split('-')
    day = int(day)
    month = int(month)
    year = int(year)
    day += 1
    if day > 31:
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1
    return f'{year}-{month:02}-{day:02}'



def get_timetable(date):
    res = requests.get(f"https://www.classcharts.com/apiv2student/timetable/{CLASSCHARTS_STUDENT_ID}?date={date}", headers={
        "authority": 'www.classcharts.com',
        "accept": 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        "authorization": CLASSCHARTS_AUTHORIZATION,
        "dnt": '1',
        "referer": 'https://www.classcharts.com/mobile/student',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    })
    return res.json()["data"]


def add_event(title, location, description, start_time, end_time):
    res = requests.post("https://outlook.office365.com/owa/service.svc?action=CreateCalendarEvent&app=Calendar", headers={
    "Accept": '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    "Connection": 'keep-alive',
    "Cookie": OUTLOOK_COOKIES.strip(),
    "DNT": '1',
    "Origin": 'https://outlook.office365.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    "action": 'CreateCalendarEvent',
    'content-type': 'application/json; charset=utf-8',
    "prefer": 'exchange.behavior="IncludeThirdPartyOnlineMeetingProviders"',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'x-owa-canary': OUTLOOK_COOKIES.split('X-OWA-CANARY=')[1].split(';')[0],
    'x-req-source': 'Calendar'
    }, json={
    "__type": "CreateItemJsonRequest:#Exchange",
    "Header": {
        "__type": "JsonRequestHeaders:#Exchange",
        "RequestServerVersion": "V2018_01_08",
        "TimeZoneContext": {
            "__type": "TimeZoneContext:#Exchange",
            "TimeZoneDefinition": {
                "__type": "TimeZoneDefinitionType:#Exchange",
                "Id": "GMT Standard Time"
            }
        }
    },
    "Body": {
        "__type": "CreateItemRequest:#Exchange",
        "Items": [
            {
                "__type": "CalendarItem:#Exchange",
                "FreeBusyType": "Busy",
                "ParentFolderId": {
                    "Id": OUTLOOK_CALENDAR_ID,
                    "mailboxInfo": {
                        "mailboxRank": "Coprincipal",
                        "mailboxSmtpAddress": OUTLOOK_EMAIL,
                        "sourceId": f"main:m365:{OUTLOOK_EMAIL}",
                        "type": "UserMailbox",
                        "userIdentity": OUTLOOK_EMAIL
                    }
                },
                "Sensitivity": "Normal",
                "Subject": title,
                "Body": {
                    "BodyType": "HTML",
                    "Value": f"<div style=\"font-family: Calibri, Arial, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);\" class=\"elementToProof\">{description}</div>"
                },
                "Start": start_time,
                "End": end_time,
                "IsAllDayEvent": False,
                "ReminderMinutesBeforeStart": 5, # change this if u want ig
                "ReminderIsSet": True,
                "CharmId": 57,
                "MuteNotifications": False,
                "CalendarEventClassifications": [],
                "Resources": [],
                "Locations": [
                    {
                        "Id": location,
                        "DisplayName": location
                    }
                ],
                "IsDraft": False,
                "DoNotForwardMeeting": False,
                "IsResponseRequested": True,
                "StartTimeZoneId": "GMT Standard Time",
                "EndTimeZoneId": "GMT Standard Time",
                "HideAttendees": False,
                "AppendOnSend": [],
                "PrependOnSend": [],
                "IsBookedFreeBlocks": False,
                "AssociatedTasks": [],
                "CollabSpace": None,
                "DocLinks": [],
                "ItemId": {
                    "__type": "ItemId:#Exchange",
                    "Id": str(uuid.uuid4()),
                    "mailboxInfo": {
                        "mailboxRank": "Coprincipal",
                        "mailboxSmtpAddress": OUTLOOK_EMAIL,
                        "sourceId": f"main:m365:{OUTLOOK_EMAIL}",
                        "type": "UserMailbox",
                        "userIdentity": OUTLOOK_EMAIL
                    }
                },
                "EffectiveRights": {
                    "Read": True,
                    "Modify": True,
                    "Delete": True,
                    "ViewPrivateItems": True
                },
                "IsOrganizer": True,
                "ExtendedProperty": []
            }
        ],
        "SavedItemFolderId": {
            "__type": "TargetFolderId:#Exchange",
            "BaseFolderId": {
                "__type": "FolderId:#Exchange",
                "Id": OUTLOOK_CALENDAR_ID
            }
        },
        "ClientSupportsIrm": True,
        "UnpromotedInlineImageCount": 0,
        "ItemShape": {
            "__type": "ItemResponseShape:#Exchange",
            "BaseShape": "IdOnly"
        },
        "SendMeetingInvitations": "SendToNone",
        "OutboundCharset": "AutoDetect",
        "UseGB18030": False,
        "UseISO885915": False
    }
    })
    print(res.status_code)


