import json, urllib.request

class GeoIP:
	def __init__(self, channel):
		self.channel = channel
		self.matched = False
		self.json = {}

	def match(self):
		try:
			r = urllib.request.urlopen("https://freegeoip.app/json/{}".format(self.channel.ipAddress))
			self.json = json.loads(r.read())
			r.close()
			self.matched = True
			return True
		except:
			return False