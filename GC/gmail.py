from __future__ import print_function
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/gmail.send'
from_email = 'borislav.dragandzhikov@novarto.com'
to_email = 'borislav.dragandzhikov@novarto.com'

colorcodes = {1: 11, 2: 9, 3: 5}
wordcodes =  {1: 'off.', 2: 'out of office.', 3: "not available."}

def setup():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()))

def create_message(subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(message):
    try:
        message = (mail.users().messages().send(userId=from_email, body=message)
                   .execute())
        print('Message Id: {}'.format(message['id']))
        return message
    except Exception as e:
        print('An error occurred: {}'.format(e))

mail = setup()
send_message(create_message("TEST", "It\'s just a test."))
