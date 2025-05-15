from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from static import SENDER_PASSWORD, SENDER_EMAIL


def send_email(to, subject, body):
    event_summary = body.get('summary', 'Appointment')
    description = body.get('description', '')
    start_time = body['start']['dateTime'].replace('T', ' ')[:16]
    end_time = body['end']['dateTime'].replace('T', ' ')[:16]
    calendar_link = 'https://calendar.google.com/calendar/embed?src=100tepler%40gmail.com&ctz=Asia%2FJerusalem'

    html_content = f"""
    <html>
        <body>
            <h2>{event_summary}</h2>
            <p>{description}</p>
            <p><strong>Start:</strong> {start_time}</p>
            <p><strong>End:</strong> {end_time}</p>
            <p>
                <a href="{calendar_link}" target="_blank" 
                   style="background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">
                    View in Google Calendar
                </a>
            </p>
        </body>
    </html>
    """

    body = str(body)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    part = MIMEText(html_content, 'html')
    msg.attach(part)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("Logged in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Error sending email:", e)
        