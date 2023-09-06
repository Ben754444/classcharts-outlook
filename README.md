# classcharts-outlook
a quick script to copy your classcharts timetable to outlook

> note: this script is a one-time move, it does not perform any updates/checks, and will add duplicate events if you modify the last_date file

# environment variables
this script was developed to work around an industrial quantity of restrictions, so it should work anywhere

to get the value of most variables below, you need to login to the applicable service and inspect request payloads and headers


| variable | description |
| --- | --- |
| `CLASSCHARTS_AUTHORIZATION` | authorization header sent when viewing your timetable |
| `CLASSCHARTS_STUDENT_ID` | can be found in the timetable api url (/timetable/**00000000**) |
| `OUTLOOK_CALENDAR_ID` | in the create calendar request, it exists at `Body.SavedItemFolderId.BaseFolderId.Id` in the payload |
| `OUTLOOK_COOKIES` | entire cookie header sent when creating events |
| `OUTLOOK_EMAIL` |  |
| `DAYS_TO_FETCH` | number of days to copy (includes weekends and the 31st day of every month) |


