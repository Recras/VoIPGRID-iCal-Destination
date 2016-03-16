import collections
from icalendar import Calendar, Event
from datetime import datetime
from datetime import date
from os import getenv
from threading import Timer, Thread
from time import sleep
from flask import Flask, render_template, request
import requests

class Scheduler(object):
    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

app = Flask(__name__)


lookup = {}
icalurl = getenv('ICALURL')
if not icalurl:
    print 'export ICALURL env-var'
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
    refresh()
    scheduler = Scheduler(int(getenv('POLL_TIME',60)), refresh)
    scheduler.start()
    port = int(getenv('PORT',5000))
    app.run(host= '0.0.0.0', port=port)
    scheduler.stop()
