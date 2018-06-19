import json

class xbee(object):
    def __init__(self, USB):
        self.timestamp = ''
        self.challenge = 'speed'
        self.latitude = 'HDDD.DDDDDD'
        self.longitude = 'HDDD.DDDDDD'
        self.takeoff = '0'
        self.flying = '0'
        self.landing = '0'

    def set_challenge(self, chal='N'):
    	self.challenge = chal

    def set_latlong(self, latitude, longitude):
    	self.latitude = latitude
    	self.longitude = longitude

    def set_takeoff(self, take):
    	self.takeoff = take

    def set_flying(self, fly):
    	self.flying = fly

    def set_landing(self, land):
    	self.landing = land

    def send(self):
        return json.dumps(self, default=jsonDefault)


def jsonDefault(object):
    return object.__dict__
