import os, json, time, datetime, threading, asyncio, traceback, functools
from server.rooms.Rooms import *
from server.users.Users import *
from server.users.Commands import *
from server.users.Skills import *
from server.users.Shop import *
from server.users.ModoPwet import *
from server.users.Inventory import *
from server.users.Missions import *
from server.tribulle.Tribulle import *
from server.helpers.API import *
from server.helpers.Langues import *
from server.helpers.Captcha import *
from server.helpers.Timer import *
from server.helpers.String import *
from server.database.Database import *
from server.cache.ManageCache import *
from server.dos.DoS import *
from server.machine.Machine import *
from network.ClientHandler import *
from network.packet.PacketManage import *
from server.xenforo.Xenforo import *
from server.discord.Discord import *
from server.swf.GameSWF import *

class Server(asyncio.BaseTransport):
	def __init__(self):
		self.ports = []
		self.clients = []
		self.config = json.loads(open("./json/config.json", "r").read())
		self.shopList = json.loads(open("./json/shoplist.json", "r").read())
		self.words = json.loads(open("./json/words.json", "r").read())
		self.mutes = json.loads(open("./json/mutes.json", "r").read())
		self.bans = json.loads(open("./json/bans.json", "r").read())
		self.visuDone = {}
		self.startServer = 0
		self.langues = None
		self.captcha = None
		self.database = None
		self.rooms = None
		self.users = None
		self.tribulle = None
		self.cache = None
		self.dos = None
		self.api = None
		self.modopwet = None
		self.firewall = None
		self.machine = None
		self.xenforo = None
		self.discord = None
		self.chats = {}
		self.ipBans = {}
		self.gameSWF = None

	def set_protocol(self):
		return self

	def start(self):
		self.cache = ManageCache()
		self.println("Connecting to database...", "info")
		self.database = Database(self)
		if self.database.connect():
			self.startServer = self.getTime()
			self.println("Starting server...", "info")
			self.langues = Langues()
			self.captcha = Captcha(self)
			self.users = Users(self)
			# emails list
			#pool = self.database.execute("SELECT * FROM users")
			#results = self.database.fetchall(pool)
			#for row in results:
			#	if not row["Email"] in list(self.cache.usersByEmail):
			#		self.cache.usersByEmail[row["Email"]] = []
			#	self.cache.usersByEmail[row["Email"]].append("{}#{}".format(row["playerName"], row["playerTag"]))
			self.rooms = Rooms(self, self.users)
			self.users.packetManage = PacketManage(self.users)
			self.users.commands = Commands(self.users, self.rooms)
			self.users.skills = Skills(self.users, self.rooms)
			self.users.shop = Shop(self.users)
			self.users.inventory = Inventory(self.users)
			self.users.missions = Missions(self.users)
			#self.users.updateSeasonRanking()
			self.tribulle = TribulleServer(self, self.users)
			self.dos = DoS(self)
			self.machine = Machine(self)
			self.machine.start()
			self.api = API(self)
			self.api.start()
			self.modopwet = ModoPwet(self)
			self.xenforo = Xenforo(self)
			#self.gameSWF = GameSWF(self)
			#self.gameSWF.start()
			self.discord = Discord
			self.discord.setServer(self)
			self.println("Server loaded in: {}ms".format(int(self.getTime() * 1000 - self.startServer * 1000)), "info");
			loop = asyncio.get_event_loop()
			bound_protocol = functools.partial(ClientHandler, self)
			for port in self.config["ports"]:
				coro = loop.create_server(bound_protocol, "0.0.0.0", int(port))
				server = loop.run_until_complete(coro)
				self.ports.append(int(port))
			self.saveJsonFiles()
			self.println("Server online on ports: {}\n".format(self.ports), "info")
			self.println("Connecting to Discord API...", "info")
			self.discord.run("NjQ2MDg0MzIxNzYwNzcyMTI3.Xorx5Q.RZr3oZVbGpviAEizFq63ovVgf-w")
			loop.run_forever()

	def println(self, message, type_):
		today = datetime.date.today()
		print("[{}] [{}] {}".format(today, type_, message))

	def getTime(self):
		return time.time()

	def getHoursDiff(self, endTimeMillis):
		startTime = self.getTime()
		startTime = datetime.datetime.fromtimestamp(float(startTime))
		endTime = datetime.datetime.fromtimestamp(float(endTimeMillis))
		result = endTime - startTime
		seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
		hours = int(int(seconds) / 3600) + 1
		return hours

	def saveJsonFiles(self):
		json.dump(self.config, open("./json/config.json", "w"))
		json.dump(self.words, open("./json/words.json", "w"))
		json.dump(self.mutes, open("./json/mutes.json", "w"))
		json.dump(self.bans, open("./json/bans.json", "w"))
		json.dump(self.rooms.records, open("./json/records.json", "w"))
		json.dump(self.dos.ipBlocks, open("./json/dos.json", "w"))
		t = threading.Timer(60, self.saveJsonFiles)
		t.start()