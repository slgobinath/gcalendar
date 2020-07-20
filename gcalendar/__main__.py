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
from datetime import datetime, timezone
from os.path import join

from dateutil.relativedelta import relativedelta
from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error
from oauth2client import client
from oauth2client import clientsecrets

from gcalendar import DEFAULT_CLIENT_ID, DEFAULT_CLIENT_SECRET, TOKEN_STORAGE_VERSION, VERSION
from gcalendar.gcalendar import GCalendar

# the home folder
HOME_DIRECTORY = os.environ.get('HOME') or os.path.expanduser('~')

# ~/.config/gcalendar folder
CONFIG_DIRECTORY = os.path.join(os.environ.get(
    'XDG_CONFIG_HOME') or os.path.join(HOME_DIRECTORY, '.config'), 'gcalendar')

TOKEN_FILE_SUFFIX = "_" + TOKEN_STORAGE_VERSION + ".dat"


def validate_account_id(account_id):
    """
    Validate the argparse argument --account
    """
    account = str(account_id)
    if not account.isalnum():
        raise argparse.ArgumentError("--account", "%s is not an alphanumeric id" % account)
    return account


def delete_if_exist(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def list_accounts():
    accounts = list()
    for file in os.listdir(CONFIG_DIRECTORY):
        if os.path.isfile(join(CONFIG_DIRECTORY, file)) and file.endswith(TOKEN_FILE_SUFFIX):
            accounts.append(file.replace(TOKEN_FILE_SUFFIX, ""))
    return accounts


def reset_account(account_id, storage_path):
    if os.path.exists(storage_path):
        delete_if_exist(storage_path)
        if os.path.exists(storage_path):
            return "Failed to reset %s" % account_id
        else:
            return "Successfully reset %s" % account_id
    else:
        return "Account %s does not exist" % account_id


def handle_error(error, message, output_type, debug_mode):
    if output_type == "txt":
        print("\033[91m" + message + "\033[0m")
    elif output_type == "json":
        print('{"error": "%s"}' % message)
    if debug_mode:
        raise error


def print_status(status, output_type):
    if output_type == "txt":
        print(status)
    elif output_type == "json":
        print('{"status": "%s"}' % status)


def print_list(obj_list, output_type):
    if output_type == "txt":
        for acc in obj_list:
            print(acc)
    elif output_type == "json":
        print(json.dumps(obj_list))


def print_events(events, output_type):
    if output_type == "txt":
        for event in events:
            print("%s:%s - %s:%s\t%s\t%s" % (
                event["start_date"], event["start_time"], event["end_date"], event["end_time"], event["summary"],
                event["location"]))
    elif output_type == "json":
        print(json.dumps(events))


def main():
    """
    Retrieve Google Calendar events.
    """
    parser = argparse.ArgumentParser(prog='gcalendar', description="Read your Google Calendar events from terminal.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list-calendars", action="store_true", help="list all calendars from the Google account")
    group.add_argument("--list-accounts", action="store_true", help="list the id of gcalendar accounts")
    group.add_argument("--status", action="store_true", help="print the status of the gcalendar account")
    group.add_argument("--reset", action="store_true", help="reset the the account")
    parser.add_argument("--calendar", type=str, default=["*"], nargs="*", help="calendars to list events from")
    parser.add_argument("--no-of-days", type=str, default="7", help="number of days to include")
    parser.add_argument("--account", type=validate_account_id, default="default",
                        help="an alphanumeric name to uniquely identify the account")
    parser.add_argument("--output", choices=["txt", "json"], default="txt", help="output format")
    parser.add_argument("--client-id", type=str, help="the Google client id")
    parser.add_argument("--client-secret", type=str,
                        help="the Google client secret")
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    parser.add_argument("--debug", action="store_true", help="run gcalendar in debug mode")
    args = parser.parse_args()

    # Create the config folder if not exists
    if not os.path.exists(CONFIG_DIRECTORY):
        os.mkdir(CONFIG_DIRECTORY)

    account_id = args.account
    storage_path = join(CONFIG_DIRECTORY, account_id + TOKEN_FILE_SUFFIX)

    if args.list_accounts:
        # --list-accounts
        print_list(list_accounts(), args.output)
        return 0

    elif args.reset:
        # --reset
        status = reset_account(account_id, storage_path)
        print_status(status, args.output)
        return 0

    elif args.status:
        # --status
        if os.path.exists(storage_path):
            if GCalendar.is_authorized(storage_path):
                status = "Authorized"
            else:
                status = "Token Expired"
        else:
            status = "Not authenticated"
        print_status(status, args.output)
        return 0

    else:
        # Extract arguments
        no_of_days = int(args.no_of_days)
        client_id = args.client_id
        client_secret = args.client_secret
        selected_calendars = [x.lower() for x in args.calendar]

        current_time = datetime.now(timezone.utc).astimezone()
        time_zone = current_time.tzinfo
        start_time = str(current_time.isoformat())
        end_time = str((current_time + relativedelta(days=no_of_days)).isoformat())

        if not client_id or not client_secret:
            client_id = DEFAULT_CLIENT_ID
            client_secret = DEFAULT_CLIENT_SECRET

        try:
            g_calendar = GCalendar(client_id, client_secret, account_id, storage_path)
            if args.list_calendars:
                print_list(g_calendar.list_calendars(), args.output)
            else:
                calendar_events = g_calendar.list_events(selected_calendars, start_time, end_time, time_zone)
                print_events(calendar_events, args.output)
            return 0

        except clientsecrets.InvalidClientSecretsError as ex:
            handle_error(ex, "Invalid Client Secrets", args.output, args.debug)

        except client.AccessTokenRefreshError as ex:
            handle_error(ex, "Failed to refresh access token", args.output, args.debug)

        except HttpLib2Error as ex:
            if "Unable to find the server at" in str(ex):
                msg = "Unable to find the Google Calendar server. Please check your connection."
            else:
                msg = "Failed to connect Google Calendar"
            handle_error(ex, msg, args.output, args.debug)

        except HttpError as ex:
            if "Too Many Requests" in str(ex):
                msg = "You have reached your request quota limit. Please try gcalendar after a few minutes."
            else:
                msg = "Failed to connect Google Calendar"

            handle_error(ex, msg, args.output, args.debug)

        except BaseException as ex:
            handle_error(ex, "Failed to connect Google Calendar", args.output, args.debug)

        return -1


if __name__ == "__main__":
    main()
