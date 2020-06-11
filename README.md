# gcalendar

A command-line tool to read your Google Calendar events in JSON format.

## Run from Source

```shell script
sudo apt install python3-pip python3-setuptools python3-dateutil python3-oauth2client python3-googleapi
git clone https://github.com/slgobinath/gcalendar.git
cd gcalendar
python3 -m gcalendar
```

## Help

```shell script
usage: gcalendar [-h] [--no-of-days NO_OF_DAYS]
                   [--calendar [CALENDAR [CALENDAR ...]]] [--list-calendars]
                   [--client-id CLIENT_ID] [--client-secret CLIENT_SECRET]
                   [--account ACCOUNT]

Retrieve Google Calendar events.

optional arguments:
  -h, --help            show this help message and exit
  --no-of-days NO_OF_DAYS
                        number of days to include
  --calendar [CALENDAR [CALENDAR ...]]
  --list-calendars
  --client-id CLIENT_ID
                        the Google client id
  --client-secret CLIENT_SECRET
                        the Google client secret
  --account ACCOUNT     a name to uniquely identify the account
```

### List Calendars

```shell script
gcalendar --list-calendar
```

### List Events

```shell script
# list next 7 days events
gcalendar

# list next 30 days events
gcalendar --no-of-days 30

# list events from selected calendar
gcalendar --calendar "Holidays in Canada"
```

### Separate Accounts

```shell script
# the default account
gcalendar

# different account named foo
gcalendar --account foo

# different account named bar
gcalendar --account bar
```
## License

GNU General Public License v3