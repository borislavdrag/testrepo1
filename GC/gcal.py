from __future__ import print_function
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from oauth2client import tools
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
wordcodes =  {1: 'off', 2: 'out of office', 3: "not available"}

def setup():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store, flags)
    return build('calendar', 'v3', http=creds.authorize(Http())), build('gmail', 'v1', http=creds.authorize(Http()))

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

def add_event():
    color = colorcodes[type]
    word = wordcodes[type]

    event = {
      'summary': name,
      'description': name + ' is ' + word,
      'colorId': color,
      'start': {
        'date': from_date.strftime('%Y-%m-%d'),
      },
      'end': {
        'date': to_date.strftime('%Y-%m-%d'),
      }
    }

    event = calendar.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    send_message(create_message("TEST", name + ' is ' + word + ' from ' + event['start']['date'] + ' to ' + event['end']['date'] + '.'))

def del_event():
    now = datetime.utcnow()
    then = now + timedelta(20)
    events_result = calendar.events().list(calendarId='primary', timeMin=now.isoformat() + 'Z',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime', timeMax=then.isoformat() + 'Z').execute()

    events = events_result.get('items', [])
    id = ""
    e = ""
    for event in events:
        if event['summary'] == name and event['start']['date'] == from_date.strftime('%Y-%m-%d'):
            id = event['id']
            e = event
            break

    if id:
        calendar.events().delete(calendarId='primary', eventId=id).execute()
        send_message(create_message("TEST", name + '\'s time ' + wordcodes[type] + ' from ' + e['start']['date'] + ' to ' + e['end']['date'] + ' was cancelled.'))
    else:
        print("Event not found.")

def edit_event():
    new_from_date = datetime.strptime(sys.argv[5].split()[0], '%d%m%y')
    new_to_date = datetime.strptime(sys.argv[5].split()[1], '%d%m%y')
    new_type = int(sys.argv[6])

    color = colorcodes[new_type]
    word = wordcodes[new_type]

    now = datetime.utcnow()
    then = now + timedelta(20)

    events_result = calendar.events().list(calendarId='primary', timeMin=now.isoformat() + 'Z',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime', timeMax=then.isoformat() + 'Z').execute()

    events = events_result.get('items', [])
    e = ""
    for event in events:
        if event['summary'] == name and event['start']['date'] == from_date.strftime('%Y-%m-%d'):
            e = event
            break

    if e:
        send_message(create_message("TEST", name + '\'s time ' + wordcodes[type] + ' from ' + e['start']['date'] + ' to ' + e['end']['date'] + ' was changed to time ' + word + ' from ' + new_from_date.strftime('%Y-%m-%d') + ' to ' + new_to_date.strftime('%Y-%m-%d') + '.'))
        e.update({
          'description': e['summary'] + ' is ' + word,
          'colorId': color,
          'start': {
            'date': new_from_date.strftime('%Y-%m-%d')
          },
          'end': {
            'date': new_to_date.strftime('%Y-%m-%d')
          }
        })

        updated_event = calendar.events().update(calendarId='primary', eventId=e['id'], body=e).execute()
    else:
        print("Event not found.")

if __name__ == '__main__':
    command = sys.argv[1]
    calendar, mail = setup()

    name = sys.argv[2]
    from_date = datetime.strptime(sys.argv[3].split()[0], '%d%m%y')
    to_date = datetime.strptime(sys.argv[3].split()[1], '%d%m%y')
    type = int(sys.argv[4])

    if command == 'add':
        add_event()
    elif command == 'edit':
        edit_event()
    elif command == 'del':
        del_event()
