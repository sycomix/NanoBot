#!/usr/bin env python2

from NanoBot import *

# Global stuff
# Enforce UTF-8
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

# Main function when run on the command line
if __name__ == '__main__':
	
    # Master entity that is the nano; Initialize bot
    nano = NanoBot()

    # Connect to XMPP and hand off control
    nano.run()