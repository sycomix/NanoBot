from twisted.internet import reactor, protocol
import json


class Bot:
    """
    Server that loads all plugins then listens and responds on TCP
    """
    def __init__(self):
        return

    def run(self):
        print("Listening")
        factory = protocol.ServerFactory()
        factory.protocol = Kernel
        reactor.listenTCP(8008, factory)
        reactor.run()


class Kernel(protocol.Protocol):
    """
    Twisted protocol that handles incoming connection data
    and passes it to all plugins
    """

    def __init__(self):
        """
        Constructor
        """
        self.plugins = dict()
        self.load_all_plugins()

    def load_all_plugins(self):
        """
        Load all plugins
        """
        # List of plugins to load - This should be a list of file names from plugins dir
        plugin_list = ["MyModule"]

        #plugin_list = filenames in folder "./plugins/"

        # Load all plugins
        for plugin_name in plugin_list:
            # Load module
            self.plugins[plugin_name] = globals()[plugin_name]()


    def dataReceived(self, data):
        """
        # decode JSON data and pass data to each plugin
        """
        # Turn JSON input in to object
        data = json.loads(data)

        # Process data with each plugin
        for name in self.plugins:
            print(name)
            response = self.plugins[name].process(data)
            # Break on first response
            if response:
                break

        # Send response back over wire
        self.transport.write(json.dumps(response))
