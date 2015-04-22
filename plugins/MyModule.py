class MyModule():
    """
    Example custom plugin using base plugin class
    """
    def __init__(self):
        self.name = "NanoDano's First Custom NanoBot Plugin"
        print("My custom module was inited!")

    def pre_process(self, data):
        return

    def process(self, data):
        print("My custom module has just processed some data: " + repr(data))

    def post_process(self, data, response):
        return