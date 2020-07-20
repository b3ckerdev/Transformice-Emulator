import threading, psutil, json, time

class Machine(threading.Thread):
	def __init__(self, server):
		threading.Thread.__init__(self)

		self.server = server
		self.lastUpdate = 0

	def run(self):
		while True:
			cpu = psutil.cpu_percent()

			if cpu >= 75:
				if int(self.server.getTime() - self.lastUpdate) > 300:
					json.dump(self.server.config, open("./json/config.json", "w"))
					json.dump(self.server.words, open("./json/words.json", "w"))
					json.dump(self.server.mutes, open("./json/mutes.json", "w"))
					json.dump(self.server.bans, open("./json/bans.json", "w"))
					json.dump(self.server.rooms.records, open("./json/records.json", "w"))

					for player in self.server.users.players.values():
						self.server.users.updateDatabase(player)

					self.lastUpdate = self.server.getTime()
					self.server.users.sendMessageToPriv(10, "The machine has a very high CPU. All server information has been saved for security ({}%).".format(int(cpu)), True)
					self.server.println("The machine has a very high CPU. All server information has been saved for security ({}%).".format(int(cpu)), "warn")

			time.sleep(10)