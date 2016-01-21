from urllib2 import urlopen
import os
import json
import datetime
from pprint import pprint

def renew():

        now = datetime.datetime.now()
        print 'Start model cache renew %s' % str(now)
	url = "http://schemas.usgin.org/contentmodels.json"

	fn = '/usr/lib/ckan/src/usginmodels/contentmodels.json'
	fntemp = '/usr/lib/ckan/src/usginmodels/contentmodels.json.tmp'

	response = urlopen(url)
	if response:
	   os.rename(fn,fntemp)
	   cb = json.load(response)
	   with open(fn,'w') as fp:
		json.dump(cb, fp)

	   fp.close()
	   os.remove(fntemp)

        now = datetime.datetime.now()
        print 'Complete model cache renew %s' % str(now)

if __name__ == "__main__":
    renew()
        