
class InvalidUri(Exception):
    def __init__(self, uri):
        self.message = "The URI %s is invalid" % uri