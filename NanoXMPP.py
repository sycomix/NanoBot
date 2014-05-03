#!/usr/bin env python2
"""
NanoXMPP
nanodano@devdungeon.com

Class that takes advantage of Reddit PRAW library to provide a handful
of useful functions for interacting with Reddit
"""
import sleekxmpp

class NanoXMPP(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        
        # Initialize ClientXMPP class
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # Register plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping

        # Some basic settings
        self.room = room
        self.nick = nick
        self.auto_authorize = True
        self.auto_subscribe = True
        
    # Handle initial startup
    def handle_session_start(self, event):
        self.get_roster()
        self.send_presence()
        # Join MUC room
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # password=the_room_password,
                                        )