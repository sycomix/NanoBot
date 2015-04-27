from twisted.internet import reactor, protocol
import json
import imp
import logging

# @TODO Make request/response objects instead of manually making json/stdobjs
# @TODO Add AIML
# @TODO Load all plugins automatically
# @TODO provide argument for plugin folder
# @TODO Accept command line options
# @TODO Rewrite so it only loads plugins ONCE instead of every request

# Logging stuff
LOG_FILENAME = 'nanobot.log.txt'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )


class NanoBotProtocol(protocol.Protocol):
    """
    Twisted protocol that handles incoming connection data
    and passes it to all plugins
    """

    def __init__(self):
        """
        Constructor
        """
        logging.info('Initializing Kernel')
        self.plugins = dict()
        self.load_all_plugins()

    def load_all_plugins(self):
        """
        Load all plugins
        """
        # List of plugins to load - This should be a list of file names from plugins dir
        plugin_list = ["MyModule"]

        #plugin_list = filenames in folder "./plugins/"
        logging.info('Loading MyModule')
        module = imp.load_source('MyModule', '/home/dtron/workspace/NanoBot/plugins/MyModule/MyModule.py')
        self.plugins['MyModule'] = module.MyModule()
        logging.info('Finished Loading MyModule')
        # Load all plugins
        #for plugin_name in plugin_list:
            # Load module
         #   self.plugins[plugin_name] = globals()[plugin_name]()

    def dataReceived(self, data):
        """
        # decode JSON data and pass data to each plugin
        """
        # Load received data
        data = json.loads(data.decode('UTF-8'))

        # Process data with each plugin
        for name in self.plugins:
            response = self.plugins[name].process(data)
            # Break on first response
            if response:
                break

        # Send response back
        self.transport.write(json.dumps(response).encode('UTF-8'))


class Bot:
    """
    Server that loads all plugins then listens and responds on TCP
    """
    def __init__(self):
        return

    def run(self):
        logging.info('Starting NanoBot')
        factory = protocol.ServerFactory()
        factory.protocol = NanoBotProtocol
        reactor.listenTCP(8008, factory)
        reactor.run()


if __name__ == '__main__':
    bot = Bot()
    bot.run()

