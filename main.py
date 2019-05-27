import collections
from icalendar import Calendar, Event
from datetime import datetime
from datetime import date
from os import getenv
from flask import Flask, render_template, request
import requests

lookup = {}
icalurl = getenv('ICALURL')
if not icalurl:
    print('export ICALURL env-var')
    quit()

def refresh():
    g = requests.get(str(icalurl))

    gcal = Calendar.from_ical(g.text)
    newlookup = {}
    for component in gcal.walk():
        summary = component.get('summary').__str__()
        if component.name == "VEVENT" and '@' in summary:
            date = component.get('dtstart').dt
            if  date >= date.today():
                atIndex = summary.find('@')
                newlookup[date] = summary[:atIndex]
    global lookup
    lookup = newlookup

def getApp():
    app = Flask(__name__)
    refresh()
    return app

app = getApp()

def getToday():
    today = date.today()
    if today in lookup:
        return lookup[today]
    return ''

@app.route('/')
def main():
    refresh()
    return render_template('overview.html', lookup=collections.OrderedDict(sorted(lookup.items())), today=getToday())


@app.route('/webhook/')
def webhook():
    return 'status=ACK&value=' + getToday()


if __name__ == "__main__":
    port = int(getenv('PORT',5000))
    if getenv('DEBUG'):
        app.debug = True
    app.run(host= '0.0.0.0', port=port)
