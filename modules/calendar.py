from datetime import datetime, timedelta

from modules.google_api import get_calendar_service
from modules.email import send_email
from static import CALENDARID, TIME_ZONE


def add_appointment(start_datetime_str, name, mail):
    service = get_calendar_service()
    start_dt = datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M")
    end_dt = start_dt + timedelta(hours=1)
    events_result = service.events().list(
        calendarId=CALENDARID,
        timeMin=start_dt.isoformat() + 'Z',
        timeMax=end_dt.isoformat() + 'Z',
        singleEvents=True,
        timeZone=TIME_ZONE,
        orderBy='startTime'
    ).execute()

    if events_result.get('items'):
        return False, "Slot already booked. Please choose a different time."

    event = {
        'summary': 'Doctor Appointment',
        'description': f'Appointment for {name}',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': TIME_ZONE},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': TIME_ZONE},
    }

    service.events().insert(calendarId=CALENDARID, body=event).execute()
    send_email(mail,"Appointment confirmation",event)
    return True, f"Appointment created: <a href='{'https://calendar.google.com/calendar/embed?src=100tepler%40gmail.com&ctz=Asia%2FJerusalem'}' target='_blank'>View in Calendar</a>"
