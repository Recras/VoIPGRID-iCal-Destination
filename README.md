VoIPGRID iCal Destination
=========================

Build the docker container with:

`docker build -t recras/voipgridicaldestination .`

Run it with:

`docker run -p 5000:5000 -e "ICALURL=https://some.url/calendar.ics" --rm recras/voipgridicaldestination`

This makes the website available at http://localhost:5000

The environment variable ICALURL should be a publicly accesible iCal-file that has full-day events containing an '@' in the summary. The part before the '@' will be used as the value.

http://localhost:5000 gives an overview of the dates & values
http://localhost:5000/webhook gives an VoIPGRID compatible webhook output with a value for the current day.

