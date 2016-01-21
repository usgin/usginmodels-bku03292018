from urllib2 import urlopen
from datetime import datetime
import json
import logging
import os


from content_model import ContentModel


log = logging.getLogger(__name__)

class ModelCache():

    models = []
    last_update = None
    url = "http://schemas.usgin.org/contentmodels.json"
   
    def __init__(self, url=None):
        if url:
            self.url = url
        self.refresh()
        
        log.info("ModelCache init for url %s", self.url)


    def refresh(self):

        log.info("ModelCache refresh  %s", self.url)
        
        localCM = open('/usr/lib/ckan/src/usginmodels/contentmodels.json', 'r')
        server_data = json.load(localCM)

        # response = urlopen(self.url)
        # server_data = json.load(response)
        
        self.models = [ContentModel(m) for m in server_data]
        self.last_update = datetime.now()
