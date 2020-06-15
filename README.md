# gcalendar

A command-line tool to read your Google Calendar events in JSON format.

## Installation

### Install from Source
```shell script
sudo apt install python3-pip python3-setuptools python3-dateutil python3-oauth2client python3-googleapi
git clone https://github.com/slgobinath/gcalendar.git
cd gcalendar
pip3 install -e .
```

## Run from Source

```shell script
sudo apt install python3-pip python3-setuptools python3-dateutil python3-oauth2client python3-googleapi
git clone https://github.com/slgobinath/gcalendar.git
cd gcalendar
python3 -m gcalendar
```

## Help

```shell script
usage: gcalendar [-h]
                 [--list-calendars | --list-accounts | --status | --reset]
                 [--calendar [CALENDAR [CALENDAR ...]]]
                 [--no-of-days NO_OF_DAYS] [--account ACCOUNT]
                 [--output {txt,json}] [--client-id CLIENT_ID]
                 [--client-secret CLIENT_SECRET] [--version]

Read your Google Calendar events from terminal.

optional arguments:
  -h, --help            show this help message and exit
  --list-calendars
  --list-accounts
  --status
  --reset               reset the the account
  --calendar [CALENDAR [CALENDAR ...]]
  --no-of-days NO_OF_DAYS
                        number of days to include
  --account ACCOUNT     an alphanumeric name to uniquely identify the account
  --output {txt,json}
  --client-id CLIENT_ID
                        the Google client id
  --client-secret CLIENT_SECRET
                        the Google client secret
  --version             show program's version number and exit
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

### Reset Accounts
```shell script
# reset the default account
gcalendar --reset

# reset the account named foo
gcalendar --account foo --reset

# reset the account named bar
gcalendar --account bar --reset
```

## License

GNU General Public License v3