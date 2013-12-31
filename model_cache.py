from urllib2 import urlopen
from datetime import datetime
import json
#from collections import OrderedDict


from content_model import ContentModel


class ModelCache():

    models = []
    last_update = None
    url = "http://127.0.0.1:8000/contentmodels.json"
    #url = "http://schemas.usgin.org/contentmodels.json"

    def __init__(self, url=None):
        if url:
            self.url = url
        self.refresh()

    def refresh(self):
        response = urlopen(self.url)
        server_data = json.load(response)
        # server_data = json.load(response, object_pairs_hook=OrderedDict)

        self.models = [ContentModel(m) for m in server_data]
        self.last_update = datetime.now()