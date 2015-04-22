NanoBot
=====

**NanoBot** is a python XMPP and AIML bot framework



Dependencies (Not included)
------
SleekXMPP: http://sleekxmpp.com/ (Available on pip)
PRAW: https://praw.readthedocs.org/en/latest/ (Available on pip)
PyAIML: http://pyaiml.sourceforge.net/ (git://pyaiml.git.sourceforge.net/gitroot/pyaiml/pyaiml)


Installation
-----

Run in terminal::

	$ git clone https://github.com/NanoDano/NanoBot
	$ python NanoBot


Usage
-----

Simple usage:

    $ python NanoBot

Scripted usage:
    $ python2 __main__.py -j nanobot@devdungeon.com -H devdungeon.com -n NanoBot -r speakeasy@conference.devdungeon.com -p `cat pass.txt` "$@"

	
To do
-----

- Provide more robust brain file checking (exists, is writable, need updating?)
- Store AIML sessions to file for persistence
- Add status presence updates
- Add database logging
- Integrate external data (db:topics, keywords)
- Add AIML++ compiler - shorthand aiml generation
- Add AIML token replacement post-process
- help me at https://github.com/NanoDano/NanoBot

Author
-----

* NanoDano <nanodano@devdungeon.com>

License
-----

* NanoBot is licensed under the *Do What The Fuck You Want to Public License*, WTFPL. See the LICENSE.txt file.


Feature list / wish list
-----
10 second trivia
who else are you talking to
what have you learned today?
private tells / store until online
Link previewer: Link detected: Title: - mime/type + size
most used words, word length, longest word, messages per day
[my|user] link post history
lmgtfy
teach/learn command
reddit bot
"reddit help"
"reddit karma nanodano"
"reddit postcount nanodano"
fortune cookie
horoscope
translate
chat
weather
word definition
word rhyme
flight status
RSS alert
bookmarks
riddles
games
Music
Mail
Messages
Calendar
Reminders
Notes
Contacts
Alarms
World Clock
Timer
Weather
Stocks
Web search
Wikipedia search
Wolfram|Alpha (English only)
Find My Friends
Post on Facebook
Twitter
Movies
Sports
App launch
Maps
Local search
search kat.ph (TORRENTS)
search yelp