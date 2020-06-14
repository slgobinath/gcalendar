# Privacy Policy

Gobinath built `gcalendar` as a Free and Open Source tool to view Google Calendar events on the terminal. This command-line tool is provided by Gobinath at no cost and is intended for use as is.

This page is used to inform visitors regarding my policies with the collection, use, and disclosure of Personal Information if anyone decided to use `gcalendar`.

`gcalendar` requires you to authorize it to access your Google calendar events. `gcalendar` requires only read permission and does not modify any of your events. OAuth tokens will be stored in your computer itself and will not be shared with anyone else. `gcalendar` uses the token to retrieve your calendar events and show them on your desktop.

**None of your data is collected, stored, processed or shared with me (the developer) or any third-parties.** You are more than welcome to check the source code or reach me out if you have any questions.

The app does rely on [Google Calendar API](https://developers.google.com/calendar/) services that may collect information used to identify you. I highly recommend you to read [Google Privacy Policy](https://policies.google.com/privacy) for more information.

## Links to Other Services

This utility **does not** contain any links to any third-party services. The only service accessed by `gcalendar` is Google Calendar. I have no control over and assume no responsibility for the content, privacy policies, or practices of Google Calendar sites or services.

## How gcalendar Works

`gcalendar` only uses the `https://www.googleapis.com/auth/calendar.readonly` scope to read your Google calendars and events from each calendar. In order to read your calendar events, you must authorize `gcalendar` as shown in this [Youtube Video](https://www.youtube.com/watch?v=mwU8AQmzIPE).

The authorized token is stored in your local machine in `~/.config/gcalendar` folder. You can revoke this token anytime by deleting those tokens from the folder manually or using `gcalendar --reset` command. Other than the token, none of your data is stored on your disk.

`gcalendar` directly reads your Google Calendar events and prints them on your terminal. **No third-party services are used in the process. None of your data is shared with the developer (Gobinath Loganathan) or any third parties. Calendar events retrieved by `gcalendar` are only formatted and printed on the terminal. There are no other operations performed on your events.**

## Changes to This Privacy Policy

I may update the Privacy Policy from time to time. Thus, you are advised to review this page periodically for any changes. I will notify you of any changes by posting the new Privacy Policy on this page. These changes are effective immediately after they are posted on this page.

## Contact

If you have any questions or suggestions about this Privacy Policy, do not hesitate to contact me at [Gobinath](https://github.com/slgobinath).
