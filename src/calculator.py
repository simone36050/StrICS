import sys
import json
import feedparser
from datetime import datetime
from ics import Calendar, Event

RSS_MIT = "http://scioperi.mit.gov.it/mit2/public/scioperi/rss"
DESCRIPTION = \
"""Modalità: {}
Sindacati: {}
Categoriea: {}
Data proclamazione: {}
Data ricezione: {}"""

def arguments():
    assert len(sys.argv) == 2, "Paramter numer mismatch"
    filters = json.loads(sys.argv[1])
    return filters

def conversion(title, summary):
    data = {}
    for segment in title.split(' - ') + summary.split('<br />'):
        key = segment.split(': ')[0].lower()
        value = segment.split(': ', 1)[1]

        if key == 'data inizio':
            data['start_date'] = value
        elif key == 'data fine':
            data['end_date'] = value
        elif key == 'settore':
            data['sector'] = value
        elif key == 'rilevanza':
            data['significant'] = value
        elif key == 'regione':
            data['region'] = value
        elif key == 'provincia':
            data['province'] = value
        elif key == 'modalità':
            data['modality'] = value
            if value.count('DALLE') == 1:
                data['start_time'] = extract_time(' DALLE', value)
                data['end_time'] = extract_time(' ALLE', value)
            else:
                data['start_time'] = None
                data['end_time'] = None
        elif key == 'sindacati':
            data['labor_unions'] = value
        elif key == 'categoria interessata':
            data['categories'] = value
        elif key == 'data proclamazione':
            data['proclamation_date'] = value
        elif key == 'data ricezione':
            data['date_of_receipt'] = value

    return data

def extract_time(key, value):
    index = value.index(key)
    length = len(key) + 1
    return value[index + length : index + length + 5]

def apply_filters(events, filters):
    if len(filters) == 0:
        return events

    new = []
    for event in events:
        for filt in filters:
            if (
                    (event['sector'].lower() == filt['sector'] or event['sector'] == 'Generale') and # sector
                    (event['significant'] == 'Nazionale' or # is national? 
                        event['region'].lower() == filt['region'] or event['province'].lower() == filt['region']) # regions
                    ):
                if event not in new:
                    new.append(event)
    return new

def convert_to_ics(event):
    ev = Event()

    # name
    if event['significant'] == 'Nazionale':
        ev.name = "Sciopero {} Nazionale".format(event['sector'])
    else:
        ev.name = "Sciopero {} {} ({})".format(event['sector'], event['region'], event['province'])

    # date and time
    ev.begin = convert_format(event['start_date'], event['start_time'])
    ev.end = convert_format(event['end_date'], event['end_time'])
    if event['start_time'] == None:
        ev.make_all_day()

    # description
    ev.description = DESCRIPTION.format(get_default(event, 'modality'), get_default(event, 'labor_unions'), 
                                        get_default(event, 'categories'), get_default(event, 'proclamation_date'),
                                        get_default(event,'date_of_receipt'))

    return ev

def get_default(event, key, default='<vuoto>'):
    if key in event:
        return event[key]
    return default

def convert_format(date, time):
    if time == '24.00':
        time = '23.59'
    return datetime \
            .strptime('{} {}'.format(date, time if time != None else '00.00'), '%d/%m/%Y %H.%M') \
            .strftime('%Y-%m-%d %H:%M:%S')

def main():
    # load RSS feed
    feed = feedparser.parse(RSS_MIT)

    # load events
    events = []
    for event in feed.entries:
        events.append(conversion(event.title, event.summary))

    # apply filters
    filters = arguments()
    events = apply_filters(events, filters)

    # create calendar
    cal = Calendar()
    for event in events:
        cal.events.add(convert_to_ics(event))

    # output calendar
    # temporary solution for timecode
    output = str(cal)
    output = output.replace('DTSTART:', 'DTSTART;TZID=Europe/Rome:')
    output = output.replace('DTEND:', 'DTEND;TZID=Europe/Rome:')
    print(output)

if __name__ == "__main__":
    main()
