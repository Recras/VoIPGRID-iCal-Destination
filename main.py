from icalendar import Calendar, Event
from datetime import datetime
from datetime import date
import requests
from os import getenv

lookup = {}

icalurl = getenv('ICALURL')
if not icalurl:
    print 'export ICALURL env-var'
    quit()

g = requests.get(str(icalurl))

gcal = Calendar.from_ical(g.text)
for component in gcal.walk():
    if component.name == "VEVENT" and '@' in component.get('summary'):
        lookup[component.get('dtstart').dt] = component.get('summary').__str__()


print 'Today: ' + lookup[date.today()]
