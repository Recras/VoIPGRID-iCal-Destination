import collections
from icalendar import Calendar, Event
from datetime import datetime
from datetime import date
from os import getenv
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


lookup = {}
icalurl = getenv('ICALURL')
if not icalurl:
    print 'export ICALURL env-var'
    quit()

def refresh():
    g = requests.get(str(icalurl))

    gcal = Calendar.from_ical(g.text)
    for component in gcal.walk():
        summary = component.get('summary').__str__()
        if component.name == "VEVENT" and '@' in summary:
            date = component.get('dtstart').dt
            if  date >= date.today():
                atIndex = summary.find('@')
                lookup[date] = summary[:atIndex]

@app.route('/')
def main():
    refresh()
    return render_template('overview.html', lookup=collections.OrderedDict(sorted(lookup.items())))


@app.route('/webhook/')
def webhook():
    return 'status=ACK&value=' + lookup[date.today()]


if __name__ == "__main__":
    refresh()
    port = int(os.environ.get('PORT',5000))
    app.run(host= '0.0.0.0', port=port)
