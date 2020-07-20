import urllib.request, base64, time, threading

class API(threading.Thread):
	def __init__(self, server):
		threading.Thread.__init__(self)
		self.server = server
		self.mapsAwait = []

	def run(self):
		while True:
			if len(self.mapsAwait) > 0:
				self.get(self.mapsAwait.pop(0))
			time.sleep(10)

	def requestDoc(self, url):
		req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'})
		doc = urllib.request.urlopen(req).read()
		return doc.decode()

	def get(self, code):
		try:
			doc = self.requestDoc("http://api.micetigri.fr/maps/xmlnew/{}".format(code))
			if not "CODE" in doc:
				return False, 0, 0, "", ""
			code = self.parse(doc, "CODE")
			perm = self.parse(doc, "PERM")
			creator = self.parse(doc, "CREATOR")
			xml = self.parse(doc, "XML")
			xml = self.decrypt(xml, "59A[XG^znsqsq8v{`Xhp3P9G")
			pool = self.server.database.execute("INSERT INTO maps (mapName, mapXML, mapPerm) VALUES (%s, %s, %s)", (creator, xml, perm))
			self.server.database.commitAll()
			pool = self.server.database.execute("SELECT * FROM maps ORDER BY mapID DESC LIMIT 1")
			results = self.server.database.fetchone(pool)
			self.server.users.sendMessageToPriv(5, "Transformice API : @{} - {} - P{} -> @{}.".format(code, creator, perm, results["mapID"]), False)
		except:
			self.server.users.sendMessageToPriv(5, "Transformice API : Error -> @{}.".format(code), False)

	def parse(self, doc, value):
		a = doc.split(value + '="')[1]
		a = a.split('"')[0]
		return a

	def decrypt(self, xml, key):
		c = int()
		xml = base64.b64decode(xml)
		end = ""
		i = 0
		while i < len(xml):
			c = xml[i]
			c = (c - int(ord(key[(i + 1) % len(key)])))
			end += chr(abs(c) & 0xFF)
			i += 1
		return end