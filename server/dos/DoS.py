import os, json

class DoS:
	def __init__(self, server):
		self.server = server

		self.ipBlocks = json.loads(open("./json/dos.json", "r").read())

		self.ipPackets = {}
		self.ipPacketsTime = {}
		self.ipConnecteds = {}
		self.ipConnectTimes = {}
		self.ipConnectCount = {}

	def new(self, ip):
		if ip in self.ipBlocks:
			return 0

		if ip in self.ipConnecteds:
			if self.ipConnecteds[ip] >= 15:
				return 1

		if ip in self.ipConnectTimes:
			if self.server.getTime() - self.ipConnectTimes[ip] < 0.5:
				if ip in self.ipConnectCount:
					self.ipConnectCount[ip] += 1
				else:
					self.ipConnectCount[ip] = 1
			else:
				self.ipConnectCount[ip] = 0
		else:
			self.ipConnectCount[ip] = 0

		if self.ipConnectCount[ip] > 15:
			self.ban(ip)
			return 2
		else:
			if ip in self.ipConnecteds:
				self.ipConnecteds[ip] += 1
			else:
				self.ipConnecteds[ip] = 1

			self.ipConnectTimes[ip] = self.server.getTime()
			return 3

	def lost(self, ip):
		if ip in self.ipConnecteds:
			self.ipConnecteds[ip] -= 1

			if self.ipConnecteds[ip] < 1:
				del self.ipConnecteds[ip]

		if self.server.getTime() - self.ipConnectTimes[ip] < 0.5:
			if ip in self.ipConnectCount:
				self.ipConnectCount[ip] += 1
			else:
				self.ipConnectCount[ip] = 1
		else:
			self.ipConnectCount[ip] = 0

		if self.ipConnectCount[ip] > 15:
			self.ban(ip)
		else:
			self.ipConnectTimes[ip] = self.server.getTime()

	def data(self, ip, data):
		if ip in self.ipPacketsTime:
			if self.server.getTime() - self.ipPacketsTime[ip] <= 0.01:
				if ip in self.ipPackets:
					self.ipPackets[ip] += 1
				else:
					self.ipPackets[ip] = 1

				if self.ipPackets[ip] >= 50:
					self.ban(ip)
					return False
			else:
				self.ipPackets[ip] = 0

		self.ipPacketsTime[ip] = self.server.getTime()
		return True

	def ban(self, ip):
		if ip in self.ipBlocks:
			return
			
		self.ipBlocks.append(ip)

		for client in self.server.clients:
			if client.ipAddress == ip:
				client.close_connection()

		os.system("netsh advfirewall firewall add rule name=\"Transformice Firewall\" interface=any dir=in action=block remoteip={}".format(ip))
		self.server.println("An attack attempt by ip {} has been blocked.".format(ip), "warn")
		self.server.users.sendMessageToPriv(10, "DoS: An attack attempt by ip {} has been blocked.".format(ip), False)

		self.vacuums(ip)

	def vacuums(self, ip):
		self.server.println("Ip {} has been added to the vacuums list.".format(ip), "warn")