import re, json, random, threading, time
from server.rooms.Room import *

class Rooms:
	def __init__(self, server, users):
		self.server = server
		self.users = users

		self.rooms = {}
		self.records = json.loads(open("./json/records.json", "r").read())
		self.roomsType = [1, 3, 8, 9, 11, 2, 10]#, 18, 16]
		self.MapList = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 90, 91, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
		self.doubleShamanMaps = [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 138, 139, 140, 141, 142, 143]
		self.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
		self.leveTestMaps = ['<C><P /><Z><S><S X="25" L="49" Y="372" H="56" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="25" L="34" Y="372" H="45" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="255" L="50" Y="376" H="50" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="254" L="15" Y="337" H="25" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="255" L="40" Y="376" H="40" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="255" L="50" Y="300" H="50" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="254" L="40" Y="300" H="40" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="253" L="19" Y="265" H="18" P="0,0,0,0.5,0,0,0,0" T="2" /><S X="759" L="63" Y="399" H="51" P="0,0,0,0.2,-40,0,0,0" T="1" /><S X="776" L="49" Y="372" H="56" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="777" L="34" Y="373" H="45" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="548" L="50" Y="375" H="50" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="549" L="40" Y="377" H="40" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="548" L="15" Y="337" H="25" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="549" L="50" Y="300" H="50" P="0,0,0.3,0.2,0,0,0,0" T="0" /><S X="550" L="40" Y="300" H="40" P="0,0,20,0.2,0,0,0,0" T="4" /><S X="549" L="19" Y="265" H="18" P="0,0,0,0.5,0,0,0,0" T="2" /><S X="251" L="470" Y="144" H="10" P="0,0,0,0.2,-60,0,0,0" T="1" /><S X="250" o="6a7495" L="28" Y="159" c="4" H="452" P="0,0,0.3,0.2,30,0,0,0" T="12" N="" /><S X="361" o="6a7495" L="28" Y="-42" c="4" H="452" P="0,0,0.3,0.2,30,0,0,0" T="12" N="" /><S X="141" L="179" Y="354" H="10" P="0,0,0.3,0.2,0,0,0,0" T="0" /></S><D><T X="25" Y="344" /><F X="777" Y="339" /></D><O /></Z></C>']

	def joinRoom(self, player, roomName):
		if not roomName in self.rooms:
			room = Room(self, roomName)
			self.rooms[roomName] = room

			self.server.println("New room: {}".format(roomName), "debug")

		room = self.rooms[roomName]
		player.room = room
		room.addClient(player)

	def leaveRoom(self, player, roomName):
		if roomName in self.rooms:
			self.rooms[roomName].removeClient(player)

	def removeRoom(self, roomName):
		del self.rooms[roomName]
		self.server.println("Removed room: {}".format(roomName), "debug")

	def getPlayersCount(self, room):
		return len(room.players)

	def getPlayersCountIP(self, room):
		ips = []
		for player in room.players.values():
			if not player.channel.ipAddress in ips:
				ips.append(player.channel.ipAddress)
		return len(ips)
		
	def getAliveCount(self, room):
		n = 0
		for player in room.players.values():
			if not player.isDead:
				n += 1
		return n

	def getHighestScore(self, room):
		highest = []
		for player in room.players.values():
			highest.append(player.playerScore)
		for player in room.players.values():
			if player.playerScore == max(highest):
				return player
		return None

	def getSecondHighestScore(self, room):
		highest = []
		for player in room.players.values():
			highest.append(player.playerScore)
		highest.remove(max(highest))
		for player in room.players.values():
			if player.playerScore == max(highest):
				return player
		return None

	def sendAll(self, room, identifiers, packet):
		for player in room.players.values():
			self.server.users.sendPacket(player.channel, identifiers, packet)

	def sendAllOthers(self, sender, room, identifiers, packet):
		for player in room.players.values():
			if sender != player:
				self.server.users.sendPacket(player.channel, identifiers, packet)

	def sendAllOld(self, room, identifiers, packet):
		for player in room.players.values():
			self.server.users.sendOldPacket(player.channel, identifiers, packet)

	def sendAllOthersOld(self, sender, room, identifiers, packet):
		for player in room.players.values():
			if sender != player:
				self.server.users.sendOldPacket(player.channel, identifiers, packet)

	def sendLangueMessageToRoom(self, room, community, langue, arguments, noPlayer=None):
		for player in room.players.values():
			if player != noPlayer:
				self.users.sendLangueMessage(player.channel, community, langue, arguments)
				
	def getRecommendRoom(self, langue, roomName=""):
		if roomName != "":
			if roomName[:1] == "*":
				langue = ""
				
			if "{}-{}".format(langue, roomName) in self.rooms:
				if self.getPlayersCount(room) < 25:
					return roomName
			else:
				return roomName

		x = 0
		while True:
			x += 1

			if x > 5:
				roomName = "{}-vanilla{}".format(langue, x)
			else:
				roomName = "{}-{}".format(langue, x)

			if roomName in self.rooms:
				room = self.rooms[roomName]
				if self.getPlayersCount(room) >= 25:
					continue

			return roomName[3:]

	def selectMap(self, room):
		villageMaps = False

		if room.leveTest:
			room.currentMap = 2020
			room.currentName = "Dumbledore"
			room.currentXML = random.choice(self.leveTestMaps)
			room.currentPerm = 17
			return

		if room.isTutorial:
			room.currentMap = 900
			return

		if room.isVanilla:
			room.currentMap = random.choice(self.MapList)
			return

		if room.isVillage:
			room.currentMap = 0
			room.currentName = "Atelier801"
			room.currentXML = '<C><P D="x_transformice/x_salon801/x_place.jpg,1600,400;x_transformice/x_salon801/x_jardin1.jpg,800,400;x_transformice/x_salon801/x_bar.jpg,2400,400;x_transformice/x_salon801/x_jardin2.jpg,0,400;x_transformice/x_salon801/x_resto.jpg,2400,0;x_transformice/x_salon801/x_pont.jpg,1600,0;x_transformice/x_salon801/x_sona.jpg,800,0;x_transformice/x_salon801/x_ciel.jpg,0,0" H="800" L="3200" APS="x_transformice/x_salon801/x_av_jardin.png,1,0,0,0,0,0,608;x_transformice/x_salon801/x_ap_cabane.png,0,2182,0,581,271,2165,0;x_transformice/x_salon801/x_ap_cabane2.png,0,1515,46,275,181,1472,38;x_transformice/x_salon801/x_av_sona.png,1,0,0,0,0,859,0" /><Z><S><S m="" P="0,0,0.3,0.2,0,0,0,0" L="200" o="12bd94" X="1739" H="25" Y="788" T="12" /><S m="" P="0,0,0.3,0.2,-90,0,0,0" L="800" o="12bd94" X="-9" H="20" Y="400" T="12" /><S m="" P="0,0,0.3,0.2,-90,0,0,0" L="800" o="12bd94" X="3210" H="20" Y="401" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2037" H="10" Y="708" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="300" o="12bd94" X="1988" H="25" Y="799" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="280" o="12bd94" X="2276" H="25" Y="786" T="12" /><S m="" P="0,0,0.3,0.2,-20,0,0,0" L="40" o="12bd94" X="2121" H="10" Y="785" T="12" /><S m="" P="0,0,0.3,0.2,20,0,0,0" L="40" o="12bd94" X="1855" H="10" Y="786" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="230" o="12bd94" X="2213" H="10" Y="664" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2191" H="10" Y="549" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2358" H="10" Y="548" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="160" o="12bd94" X="1718" H="10" Y="608" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="65" o="12bd94" X="1705" H="10" Y="547" T="12" /><S m="" P="0,0,0,0.2,38,0,0,0" L="100" o="12bd94" X="1794" H="10" Y="476" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="80" o="12bd94" X="1877" H="10" Y="519" T="12" /><S m="" P="0,0,0,0.2,-62,0,0,0" L="100" o="12bd94" X="2095" H="10" Y="523" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="65" o="12bd94" X="1827" H="10" Y="706" T="12" /><S m="" P="0,0,0.3,0.2,-18,0,0,0" L="100" o="12bd94" X="2455" H="25" Y="774" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="260" o="12bd94" X="2629" H="25" Y="760" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2596" H="10" Y="712" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2674" H="10" Y="712" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="25" o="12bd94" X="2635" H="10" Y="704" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="25" o="12bd94" X="2638" H="10" Y="522" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="25" o="12bd94" X="2938" H="10" Y="520" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="25" o="12bd94" X="3075" H="10" Y="521" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2568" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="280" o="12bd94" X="2648" H="10" Y="569" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2601" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2678" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2711" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2897" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2977" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="3036" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="3115" H="10" Y="529" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="290" o="12bd94" X="2998" H="10" Y="569" T="12" /><S m="" P="0,0,0.3,0.2,40,0,0,0" L="50" o="12bd94" X="2770" H="25" Y="773" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="430" o="12bd94" X="3002" H="25" Y="788" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2821" H="10" Y="740" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2856" H="10" Y="740" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="200" o="12bd94" X="3039" H="10" Y="719" T="12" /><S m="" P="0,0,,,,0,0,0" L="60" X="3172" H="420" Y="579" T="9" /><S m="" P="0,0,0.3,0.2,-55,0,0,0" L="175" o="12bd94" X="2807" H="10" Y="638" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="50" o="12bd94" X="2483" H="285" Y="543" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="350" o="12bd94" X="2333" H="10" Y="401" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="730" o="12bd94" X="2778" H="10" Y="385" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2590" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2677" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2732" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2821" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2878" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2968" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="3020" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="3109" H="10" Y="344" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2635" H="10" Y="335" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2779" H="10" Y="335" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2927" H="10" Y="335" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="3069" H="10" Y="335" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="50" o="12bd94" X="1684" H="10" Y="398" T="12" /><S m="" P="0,0,0.3,0.2,-30,0,0,0" L="80" o="12bd94" X="3165" H="10" Y="203" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="40" o="12bd94" X="2514" H="10" Y="333" T="12" /><S m="" P="0,0,0.3,0.2,40,0,0,0" L="40" o="12bd94" X="2484" H="10" Y="321" T="12" /><S m="" P="0,0,0.3,0.2,60,0,0,0" L="95" o="12bd94" X="2446" H="10" Y="267" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="230" o="12bd94" X="2312" H="10" Y="229" T="12" /><S m="" P="0,0,0.3,0.2,-45,0,0,0" L="60" o="12bd94" X="2328" H="10" Y="168" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="110" o="12bd94" X="2405" H="10" Y="144" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="90" o="12bd94" X="2228" H="10" Y="158" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="80" o="12bd94" X="2410" H="10" Y="124" T="12" /><S m="" P="0,0,0.3,0.2,-90,0,0,0" L="60" o="12bd94" X="2455" H="10" Y="140" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="250" o="12bd94" X="2326" H="10" Y="53" T="12" /><S m="" P="0,0,0.3,0.2,-70,0,0,0" L="90" o="12bd94" X="2186" H="10" Y="91" T="12" /><S m="" P="0,0,0.3,0.2,60,0,0,0" L="30" o="12bd94" X="2179" H="10" Y="146" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="30" o="12bd94" X="2218" H="10" Y="141" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2194" H="10" Y="134" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2242" H="10" Y="134" T="12" /><S m="" P="0,0,0.3,0.2,-15,0,0,0" L="90" o="12bd94" X="2162" H="10" Y="248" T="12" /><S m="" P="0,0,0.3,0.2,-10,0,0,0" L="90" o="12bd94" X="2076" H="10" Y="268" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="90" o="12bd94" X="1988" H="10" Y="277" T="12" /><S m="" P="0,0,0.3,0.2,10,0,0,0" L="90" o="12bd94" X="1904" H="10" Y="271" T="12" /><S m="" P="0,0,0.3,0.2,30,0,0,0" L="60" o="12bd94" X="1789" H="10" Y="237" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="100" o="12bd94" X="1717" H="10" Y="223" T="12" /><S m="" P="0,0,0.3,0.2,-6,0,0,0" L="210" o="12bd94" X="1564" H="10" Y="227" T="12" /><S m="" P="0,0,0.3,0.2,-35,0,0,0" L="30" o="12bd94" X="2188" H="10" Y="236" T="12" /><S m="" P="0,0,0.3,0.2,-20,0,0,0" L="70" o="12bd94" X="2487" H="10" Y="102" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2526" H="10" Y="91" T="12" /><S m="" P="0,0,0.3,0.2,37,0,0,0" L="70" o="12bd94" X="2562" H="10" Y="111" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="20" o="12bd94" X="2632" H="10" Y="154" T="12" /><S m="" P="0,0,0.3,0.2,-10,0,0,0" L="20" o="12bd94" X="2696" H="10" Y="136" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="150" o="12bd94" X="2935" H="10" Y="159" T="12" /><S m="" P="0,0,0.3,0.2,20,0,0,0" L="20" o="12bd94" X="1675" H="10" Y="219" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="270" o="12bd94" X="1338" H="10" Y="238" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="60" o="12bd94" X="1278" H="10" Y="217" T="12" /><S m="" P="0,0,0.3,0.2,-40,0,0,0" L="80" o="12bd94" X="1176" H="10" Y="262" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="220" o="12bd94" X="1052" H="10" Y="278" T="12" /><S m="" P="0,0,0.3,0.2,40,0,0,0" L="100" o="12bd94" X="909" H="10" Y="250" T="12" /><S m="" P="0,0,,,,0,0,0" L="300" X="1049" H="50" Y="258" T="9" /><S m="" P="0,0,2,0.2,-3,0,0,0" L="10" o="12bd94" X="870" H="200" Y="69" T="12" /><S m="" P="0,0,0.3,0.2,-10,0,0,0" L="100" o="12bd94" X="985" H="10" Y="119" T="12" /><S m="" P="0,0,0.3,0.2,-20,0,0,0" L="100" o="12bd94" X="1078" H="10" Y="95" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="430" o="12bd94" X="1424" H="25" Y="781" T="12" /><S m="" P="0,0,0.3,0.2,20,0,0,0" L="40" o="12bd94" X="1655" H="10" Y="780" T="12" /><S m="" P="0,0,0.3,0.2,100,0,0,0" L="65" o="12bd94" X="1569" H="10" Y="699" T="12" /><S m="" P="0,0,0.3,0.2,10,0,0,0" L="40" o="12bd94" X="1571" H="10" Y="668" T="12" /><S m="" P="0,0,0.3,0.2,-40,0,0,0" L="40" o="12bd94" X="1627" H="10" Y="618" T="12" /><S m="" P="0,0,10,0.2,110,0,0,0" L="150" o="12bd94" X="1600" H="10" Y="510" T="12" /><S m="" P="0,0,0,0.2,-41,0,0,0" L="200" o="12bd94" X="1519" H="10" Y="468" T="12" /><S m="" P="0,0,2,0.2,20,0,0,0" L="100" o="12bd94" X="1173" H="10" Y="673" T="12" /><S m="" P="0,0,2,0.2,30,0,0,0" L="100" o="12bd94" X="1169" H="10" Y="751" T="12" /><S m="" P="0,0,2,0.2,10,0,0,0" L="100" o="12bd94" X="1079" H="10" Y="718" T="12" /><S m="" P="0,0,2,0.2,-10,0,0,0" L="100" o="12bd94" X="984" H="10" Y="718" T="12" /><S m="" P="0,0,2,0.2,-30,0,0,0" L="100" o="12bd94" X="893" H="10" Y="751" T="12" /><S m="" P="0,0,2,0.2,10,0,0,0" L="100" o="12bd94" X="1085" H="10" Y="649" T="12" /><S m="" P="0,0,2,0.2,-10,0,0,0" L="100" o="12bd94" X="988" H="10" Y="648" T="12" /><S m="" P="0,0,2,0.2,-20,0,0,0" L="100" o="12bd94" X="898" H="10" Y="672" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="430" o="12bd94" X="635" H="25" Y="782" T="12" /><S m="" P="0,0,0.3,0.2,30,0,0,0" L="80" o="12bd94" X="447" H="10" Y="753" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="360" o="12bd94" X="235" H="10" Y="735" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="10" o="12bd94" X="62" H="170" Y="651" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="430" o="12bd94" X="211" H="25" Y="784" T="12" /><S m="" P="0,0,1,0.2,-7,0,0,0" L="100" o="12bd94" X="183" H="10" Y="542" T="12" /><S m="" P="0,0,1,0.2,6,0,0,0" L="220" o="12bd94" X="341" H="10" Y="547" T="12" /><S m="" P="0,0,0.3,0.2,0,0,0,0" L="10" o="12bd94" X="235" H="80" Y="454" T="12" /><S m="" P="0,0,0.3,10,-30,0,0,0" L="10" o="12bd94" X="188" H="40" Y="401" T="12" /></S><D><DS Y="771" X="1930" /></D><O /></Z></C>'
			room.currentPerm = 41
			return

		perm = 0
		if room.isBootcamp:
			if room.roundsRunned <= 3:
				perm = 3
			else:
				perm = 13

			if room.roundsRunned >= 6:
				room.roundsRunned = 0

		elif room.isSurvivor:
			if room.isQuarentine:
				perm = 11
			elif room.roundsRunned <= 9:
				perm = 10
			else:
				perm = 11

			if room.roundsRunned >= 10:
				room.roundsRunned = 0

		elif room.isRacing:
			perm = random.choice([17, 38])

			room.currentInverted = random.randint(0, 10) > 5

		elif room.isDefilante:
			perm = 18

			room.currentInverted = random.randint(0, 10) > 5

		elif room.isMusic:
			perm = 19

		elif room.isNormRoom:
			if room.roundsRunned <= 2:
				perm = 4
			elif room.roundsRunned <= 4:
				perm = -1
				villageMaps = True
			elif room.roundsRunned <= 6:
				perm = 6
			elif room.roundsRunned == 7:
				perm = 7
			elif room.roundsRunned <= 8:
				perm = 1
			else:
				perm = 0

			if room.roundsRunned == 11:
				room.roundsRunned = 0

		else:
			perm = 0

		if villageMaps:
			mapID = random.choice(self.MapList)
			room.currentMap = random.choice(self.MapList)
			room.currentXML = ""
			room.currentName = ""
			room.currentPerm = perm
		else:
			if room.nextMapID > 0:
				pool = self.server.database.execute("SELECT * FROM maps WHERE mapID = %s", (room.nextMapID,))
				room.nextMapID = 0
			else:
				pool = self.server.database.execute("SELECT * FROM maps WHERE mapPerm = %s ORDER BY RAND() LIMIT 1", (perm,))
			results = self.server.database.fetchone(pool)
			if results != None:
				room.currentMap = results["mapID"]
				room.currentXML = results["mapXML"]
				room.currentName = results["mapName"]
				room.currentPerm = results["mapPerm"]
			else:
				mapID = random.choice(self.MapList)
				room.currentMap = random.choice(self.MapList)
				room.currentXML = ""
				room.currentName = ""
				room.currentPerm = perm

	def getPlayersNoDead(self, room):
		noDead = 0
		for player in room.players.values():
			if not player.isDead:
				noDead += 1
		return noDead

	def getPlayersCountForMode(self, mode):
		players = 0
		for room in self.rooms.values():
			if room.roomType == mode:
				players += self.getPlayersCount(room)
		return players

	def randVampire(self, room):
		players = []
		for playerName, player in room.players.items():
			players.append(player)

		if len(players) == 0:
			return []

		count = 1
		if len(players) >= 6:
			count = 2

		p = []
		for i in range(count):
			p.append(random.choice(players))
		return p

	def getPlayersNoVampCount(self, room):
		noDead = 0
		for player in room.players.values():
			if not player.isNewPlayer:
				if not player.isVampire:
					noDead += 1
		return noDead

	def getPlayersVampCount(self, room):
		noDead = 0
		for player in room.players.values():
			if not player.isNewPlayer:
				if player.isVampire:
					if not player.isDead:
						noDead += 1
		return noDead

	def resetMap(self, room):
		room.addTime = 0
		room.bubblesCount = 0
		room.playersInPlace = 0
		room.currentShamanCode = -1
		room.currentShamanName = ""
		room.currentShamanType = 0
		room.currentShamanLevel = 0
		room.currentShamanBadge = 0
		room.currentShamanCode2 = -1
		room.currentShamanName2 = ""
		room.currentShamanType2 = 0
		room.currentShamanLevel2 = 0
		room.currentShamanBadge2 = 0
		room.currentShamanSkills = {}
		room.currentSecondShamanSkills = {}
		room.gameStartTimeMillis = self.server.getTime()
		room.catchTheCheeseMap = False
		room.holesType = {0: 0, 1: 0, 2: 0, 3: 0}
		room.anchors = []
		room.isNoShamanMap = False
		room.vampiresList = []
		room.currentVampireCode = 0
		room.currentInverted = False
		room.vampireSelected = False
		room.vampiresRand = []
		
	def getShamanCode(self, room):
		player = self.getHighestScore(room)
		room.currentShamanCode = player.playerCode
		room.currentShamanName = f"{player.playerName}#{player.playerTag}"
		room.currentShamanType = player.shamanType
		room.currentShamanLevel = player.shamanLevel#self.server.getShamanLevelByExperience(player.shamanExp)
		room.currentShamanBadge = player.Badge
		room.currentShamanSkills = player.playerSkills
		room.currentSecondShamanSkills = {}

	def getDoubleShamanCode(self, room):
		player = self.getHighestScore(room)
		room.currentShamanCode = player.playerCode
		room.currentShamanName = self.users.parsePlayerName(player)
		room.currentShamanType = player.shamanType
		room.currentShamanLevel = player.shamanLevel#self.server.getShamanLevelByExperience(player.shamanExp)
		room.currentShamanBadge = player.Badge
		room.currentShamanSkills = player.playerSkills

		player2 = self.getSecondHighestScore(room)
		room.currentShamanCode2 = player2.playerCode
		room.currentShamanName2 = self.users.parsePlayerName(player2)
		room.currentShamanType2 = player2.shamanType
		room.currentShamanLevel2 = player2.shamanLevel#self.server.getShamanLevelByExperience(player2.shamanExp)
		room.currentShamanBadge2 = player2.Badge
		room.currentSecondShamanSkills = player2.playerSkills

	def getPlayersList(self, room):
		playersList = []
		for player in room.players.values():
			if not player.isHide:
				playersList.append(self.users.getPlayerData(player))
		return playersList

	def getSyncCode(self, room):
		player = room.players[random.choice(list(room.players))]
		room.currentSyncCode = player.playerCode
		room.currentSyncName = f"{player.playerName}#{player.playerTag}"

	def getRoundTime(self, room):
		return room.roundTime + room.addTime

	def checkIfShamanCanGoIn(self, room):
		for player in room.players.values():
			if player.playerCode != room.currentShamanCode and player.playerCode != room.currentShamanCode2 and not player.isDead:
				return False
		return True

	def changeMapTime(self, room, seconds):
		if room.changeTimer != None:
			room.changeTimer.cancel()

		for player in room.players.values():
			self.users.sendRoundTime(player.channel, seconds)

		room.changeTimer = threading.Timer(seconds, room.startMap)
		room.changeTimer.start()

	def resetAllScores(self, room):
		for player in room.players.values():
			player.playerScore = 0

	def send3SecondsAll(self, room):
		for player in room.players.values():
			self.users.sendMapAccess(player.channel, 0)

	def getDeathCountNoShaman(self, room):
		count = 0
		for player in room.players.values():
			if not player.isNewPlayer:
				if player.isDead:
					if not player.isShaman:
						count += 1
		return count

	def changeRoomMusic(self, room):
		if room.currentMusicKey != "":
			del room.musicList[room.currentMusicKey]
		if len(room.musicList) == 0:
			room.musicStartedTime = 0
			room.currentMusicKey = ""
			self.users.sendMusicVideo(room, "", "", 0, "")
		else:
			m = list(room.musicList)[0]
			music = room.musicList[m]
			s = 0
			room.musicStartedTime = self.server.getTime()
			self.users.sendMusicVideo(room, music["items"][0]["id"], music["items"][0]["snippet"]["title"], s, m)
			room.currentMusicKey = m
			room.musicTimer = threading.Timer(s, self.changeRoomMusic, args=[room])
			room.musicTimer.start()

	def parseDuration(self, duration):
		time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
		for key, count in time.items():
			time[key] = 0 if count is None else time[key]
		return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)
