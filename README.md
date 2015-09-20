NanoBot
=====

**NanoBot** is an artificial intelligence chat bot. It is written in Python and uses the XMPP protocol. It can be extended to add custom commands and other features.

Dependencies (Not included)
------

* SleekXMPP: http://sleekxmpp.com/
* PRAW: https://praw.readthedocs.org/en/latest/
* PyAIML: http://pyaiml.sourceforge.net/

Installation
-----

Run in terminal::

	$ pip install sleekxmpp aiml praw
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
- Add AIML token replacement post-process

Contact
-----

* NanoDano <nanodano@devdungeon.com>

Feature list / wish list
-----
most used words, word length, longest word, messages per day
lmgtfy
Reddit commands
Fortune cookie
Horoscope
Dictionary
Flight status
RSS alert
Riddles
Alarms/Timer
Weather
Stocks
Wikipedia search
Wolfram|Alpha
