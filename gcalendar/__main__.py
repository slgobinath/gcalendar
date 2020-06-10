#!/usr/bin/env python3
# gcalendar is a tool to read Google Calendar events from your terminal.

# Copyright (C) 2020  Gobinath

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from oauth2client import client
from oauth2client import clientsecrets

from gcalendar import DEFAULT_CLIENT_ID, DEFAULT_CLIENT_SECRET
from gcalendar.gcalendar import GCalendar

# the home folder
HOME_DIRECTORY = os.environ.get('HOME') or os.path.expanduser('~')

# ~/.config/gcalendar folder
CONFIG_DIRECTORY = os.path.join(os.environ.get(
    'XDG_CONFIG_HOME') or os.path.join(HOME_DIRECTORY, '.config'), 'gcalendar')


def validate_account_id(account_id):
    """
    Validate the argparse argument --account
    """
    account = str(account_id)
    if not account.isalnum():
        raise argparse.ArgumentTypeError(
            "%s is not an alphanumeric id" % account)
    return account


def error(message, current_time):
    print(
        '[{"calendar_color": "#ffffff", "summary": "' + message +
        '", "start_date": "%s", "start_time": "00:00", "end_date": "%s", "end_time": "00:00", "location": ""}]' % (
            current_time.date(), (current_time + relativedelta(days=1)).date()))


def main(argv):
    """
    Retrieve Google Calendar events.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve Google Calendar events.")
    parser.add_argument("--no-of-days", type=str, default="7",
                        help="number of days to include")
    parser.add_argument("--calendar", type=str, default=["*"], nargs="*")
    parser.add_argument("--list-calendars", action="store_true")
    parser.add_argument("--client-id", type=str, help="the Google client id")
    parser.add_argument("--client-secret", type=str,
                        help="the Google client secret")
    parser.add_argument("--account", type=validate_account_id, default="default",
                        help="a name to uniquely identify the account")
    args = parser.parse_args()

    # Extract arguments
    no_of_days = int(args.no_of_days)
    client_id = args.client_id
    client_secret = args.client_secret
    selected_calendars = [x.lower() for x in args.calendar]
    account_id = args.account

    current_time = datetime.now(timezone.utc).astimezone()
    time_zone = str(current_time.tzinfo)
    start_time = str(current_time.isoformat())
    end_time = str((current_time + relativedelta(days=no_of_days)).isoformat())

    if not client_id or not client_secret:
        client_id = DEFAULT_CLIENT_ID
        client_secret = DEFAULT_CLIENT_SECRET

    # Create the config folder if not exists
    if not os.path.exists(CONFIG_DIRECTORY):
        os.mkdir(CONFIG_DIRECTORY)

    try:
        g_calendar = GCalendar(client_id, client_secret, account_id, CONFIG_DIRECTORY)
        if args.list_calendars:
            for calendar in g_calendar.list_calendars():
                print(calendar)
        else:
            calendar_events = g_calendar.list_events(selected_calendars, start_time, end_time, time_zone)
            if calendar_events:
                print(json.dumps(calendar_events))
            else:
                error("NO_EVENTS_FOUND_GOOGLE_CALENDAR", current_time)

    except clientsecrets.InvalidClientSecretsError:
        error("INVALID_CLIENT_SECRETS", current_time)
    except client.AccessTokenRefreshError:
        error("FAILED_TO_REFRESH_ACCESS_TOKEN", current_time)
    except BaseException:
        error("FAILED_TO_RETRIEVE_EVENTS", current_time)


if __name__ == "__main__":
    main(sys.argv)
