import json

class xbee(object):
    def __init__(self):
        self.challenge = 'speed'
        self.latitude = 'HDDD.DDDDDD'
        self.longitude = 'HDDD.DDDDDD'


    def set_challenge(self, chal='N'):
    	self.challenge = chal

    def set_latlong(self, latitude, longitude):
    	self.latitude = latitude
    	self.longitude = longitude

    def send(self):
        return json.dumps(self, default=jsonDefault)


def jsonDefault(object):
    return object.__dict__
