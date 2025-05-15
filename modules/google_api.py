from datetime import datetime, timedelta
from google.oauth2 import service_account
import httplib2
import google_auth_httplib2
from googleapiclient.discovery import build
from static import CALENDARID, SCOPES, CREDENTIALS_FILE, TIME_ZONE


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    http = httplib2.Http(disable_ssl_certificate_validation=True)
    authed_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)
    return build('calendar', 'v3', http=authed_http, cache_discovery=False)

def get_available_days():
    service = get_calendar_service()
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=7)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDARID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    events_by_day = {}

    for event in events:
        start = event['start'].get('dateTime')
        if start:
            date_only = start[:10]
            time_only = start[11:16]
            if date_only not in events_by_day:
                events_by_day[date_only] = set()
            events_by_day[date_only].add(time_only)

    all_days = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    available_days = []

    for day in all_days:
        busy_slots = events_by_day.get(day, set())
        possible_slots = {f"{hour:02d}:00" for hour in range(9, 17)}
        if busy_slots != possible_slots:
            available_days.append(day)

    return available_days

def get_available_slots_for_day(day_str):
    service = get_calendar_service()
    date_obj = datetime.strptime(day_str, '%Y-%m-%d')
    time_zone = TIME_ZONE
    
    time_min = datetime.combine(date_obj, datetime.min.time()).isoformat() + 'Z'
    time_max = datetime.combine(date_obj, datetime.max.time()).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDARID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime',
        timeZone=TIME_ZONE
    ).execute()

    events = events_result.get('items', [])
    busy_hours = set()

    for event in events:
        start = event['start'].get('dateTime')
        if start:
            dt = datetime.fromisoformat(start)
            hour_min = dt.strftime('%H:%M')
            busy_hours.add(hour_min)

    possible_slots = [f"{hour:02d}:00" for hour in range(9, 17)]
    available_slots = [slot for slot in possible_slots if slot not in busy_hours]

    return available_slots
