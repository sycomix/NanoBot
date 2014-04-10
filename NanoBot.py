#!/usr/bin/env python
import sys
import logging
import getpass
import time
from optparse import OptionParser

from NanoLogic import *     # Command/text processing, AIML logic
from NanoXMPP import *      # Handle chat server, messages, presence


# Global config vars
bot_name = "NanoBot"
bot_master = ""
bot_cmd_prefix = "nano " # Triggers a preprocess command in message process
brain_file = "brains/standard.brn"
std_startup_file = "std-startup.xml"
default_load_command = "load aiml b"


# Global stuff
# Enforce UTF-8
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input



class NanoBot():

    def __init__(self):

        # Process and store command line arguments to self.opts
        self.optp_init()

        # Set config information
        self.bot_name = bot_name
        self.bot_cmd_prefix = bot_cmd_prefix

        # Activate LPU component to handle AI - Slow - do before XMPP
        self.lpu = NanoLogic()

        # Activate XMPP component and hand over control to XMPP stanza processing
        self.xmpp = NanoXMPP(self.opts.jid, self.opts.password, self.opts.room, self.opts.nick)

        #Set up XMPP 
        if self.xmpp.connect((self.opts.host, self.opts.port)):
            # Set up event handlers   
            self.xmpp.add_event_handler("message", self.process_message)
            self.xmpp.add_event_handler("session_start", self.xmpp.handle_session_start)
            self.xmpp.add_event_handler("groupchat_message", self.muc_message)
            self.xmpp.add_event_handler("muc::%s::got_online" % self.xmpp.room,
                                   self.muc_online)
            # Process stanzas - never returns control
            self.xmpp.process(block=True)
            
        else:
            print("Unable to connect.")



    def process_message(self, msg):
        """
        Process incoming chat message:
        - Preprocess message (check for commands)
        - Process AIML
        - Replace tokens from AIML reponse if needed
        - Send final response
        - Log incoming and outgoing message

        """
        skip_aiml = False           # Flag to skip AI processing
        response = "Words fail me." # Default response if everything fails

        # Chat/normal only, ignore muc messages, and ignore messages from self
        if msg['type'] in ('chat', 'normal') and msg['from'].bare != self.xmpp.boundjid.bare:
            
            # Preprocess commands
            # If string starts with self.bot_cmd_prefix or "HELP" treat as command 
            if msg['body'][:len(self.bot_cmd_prefix)] == self.bot_cmd_prefix or msg['body'].upper() == "HELP":
               response = False # Suppress response by default
               response = self.process_command(msg) # commands can return text, respond itself, or return False to return nothing
               skip_aiml = True

            # AIML processing
            if skip_aiml == False:
                response = self.lpu.aiml_process(msg)

            # token replacement of return
            self.token_replace(msg)

            # Log incoming message and outgoing response
            self.log_message(msg, response) # log before sending, because msg becomes response after replying
            
            # Send response if exists
            if response != False:
                msg.reply(response).send()




    def token_replace(self, msg):
        # Replace tokens like [username], [get_weather], [ext plug]
        print "Token replaceholder"




    def log_message(self, msg, response):
        # Command line logging
        logging.info(msg['from'].bare + ": " + msg['body'])
        logging.info(self.bot_name + ": " + repr(response))
        logging.debug(repr(msg)) # Debugging output

        # Database logging
        # mysql log msg/respone, time, session



    # Needs to be easily extendable to import other libraries and complex functions/algorithms
    def process_command(self, msg):
        command = msg['body'][len(self.bot_cmd_prefix):]

        available_commands = ["help", "reload", "weather", "time", "define"]

        # Help
        if command.upper() == "HELP" or msg['body'].upper() == "HELP":
            return "Use help [command] for more details.\nCommands available: " + repr(available_commands)

        # reload - AIML files reload
        if command.upper() == "RELOAD":
            msg.reply("Reloading AIML. This may take a minute.").send()
            self.lpu.aimlk.respond("load aiml b")
            return "AIML files reloaded."

        

        # Weather
        if command.upper() == "WEATHER":
            return "Today's weather: http://www.weather.com/weather/today/77373"       

        # Time
        if command.upper() == "TIME":
            return "It is currently " + time.strftime("%H:%M:%S") + "."

        # Dictionary
        if "DEFINE" in command.upper():
            raw_keywords = msg['body'][3:].replace("define", "")
            keywords = raw_keywords.strip()
            keywords = keywords.replace(" ", "%20")
            keywords = keywords.replace(":", "")
            return "Here is a link to the defition of " + raw_keywords + "  : http://www.merriam-webster.com/dictionary/" + keywords

        return False # default return



    # Handle chat room message
    def muc_message(self, msg):
        if msg['mucnick'] != self.xmpp.nick:
            self.process_muc_message(self, msg)



    # Handle chat room join stanzas
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.xmpp.nick:
            self.xmpp.send_message(mto=presence['from'].bare,
                              mbody="Welcome to the dungeon, %s %s." % (presence['muc']['role'], presence['muc']['nick']),
                              mtype='groupchat')



    # Handle muc chat messages 
    # Currently not processed by AIML
    def process_muc_message(self, mucbot, msg):

        # global message process
        # store message, who, time


        # Someone asked "How do i" or "how do you" - LMGTFY
        strings = ["HOW DO I", "HOW DO YOU", "HOW CAN I", "HOW COULD I"]
        if any (x in msg['body'].upper() for x in strings):
            self.xmpp.send_message(mto=msg['from'].bare,
                              mbody="Do you need some help? See if you can find the answer here: http://lmgtfy.com?q=" + msg['body'].replace(" ", "+"),
                              mtype='groupchat')



    def optp_init(self):
        # Setup the command line arguments.
        self.optp = OptionParser()

        # Output verbosity options.
        self.optp.add_option('-q', '--quiet', help='set logging to ERROR',
                        action='store_const', dest='loglevel',
                        const=logging.ERROR, default=logging.INFO)
        self.optp.add_option('-d', '--debug', help='set logging to DEBUG',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
        self.optp.add_option('-v', '--verbose', help='set logging to COMM',
                        action='store_const', dest='loglevel',
                        const=5, default=logging.INFO)
        
        # Bot options.
        self.optp.add_option("-j", "--jid", dest="jid",
                        help="JID to use user@example.com")
        self.optp.add_option("-p", "--password", dest="password",
                        help="password to use")
        self.optp.add_option("-r", "--room", dest="room",
                        help="MUC Room - room@conference.example.com")
        self.optp.add_option("-n", "--nick", dest="nick",
                        help="Nickname for chat")
        self.optp.add_option("-H", "--host", dest="host",
                        help="XMPP Host")
        self.optp.add_option("-P", "--port", dest="port",
                        help="XMPP Port (Default 5222)", default=5222)
        self.opts, self.args = self.optp.parse_args()

        # Set logging to use specified options
        logging.basicConfig(level=self.opts.loglevel, format='%(levelname)-8s %(message)s')

        if self.opts.host is None:
            self.opts.host = raw_input("Server host (example.com): ")
        if self.opts.jid is None:
            self.opts.jid = raw_input("Username (user@example.com): ")
        if self.opts.password is None:
            self.opts.password = getpass.getpass("Password: ")
        if self.opts.nick is None:
            self.opts.nick = raw_input("Nickname: ")
        if self.opts.room is None:
            self.opts.room = raw_input("MUC room (room@conference.example.com): ")



# Main function when run on the command line
if __name__ == '__main__':

    """
    Master entity that is the nano
    """
    nano = NanoBot()