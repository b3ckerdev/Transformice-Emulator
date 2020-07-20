from network.packet.ByteArray import *

class ModoPwet:
	def __init__(self, server):
		self.server = server
		self.reports = {"names": []}

	def getPlayerRoomName(self, playerName):
		if playerName in self.server.users.players:
			return self.server.users.players[playerName].room.roomName
		else:
			return "0"

	def getProfileCheeseCount(self, playerName):
		if playerName in self.server.users.players:
			return self.server.users.players[playerName].cheeseCount
		else:
			return 0

	def getModsRoom(self, roomName):
		mods = []
		if roomName in self.server.rooms.rooms:
			for player in self.server.rooms.rooms[roomName].players.values():
				if player.privLevel >= 5:
					mods.append(self.server.users.parsePlayerName(player))
		return mods

	def followPlayer(self, player, playerName):
		roomName = self.server.users.players[playerName].room.roomName
		if not roomName[:1] == "*":
			roomName = roomName[3:]
		self.server.users.enterRoom(player, roomName)

	def updateModoPwet(self):
		for player in self.server.users.players.values():
			if player.modoPwet and player.privLevel >= 5:
				self.openModoPwet(player)

	def sendAllMessage(self, message):
		for player in self.server.users.players.values():
			if player.modoPwetNotification and player.privLevel >= 5:
				self.server.users.sendMessage(player.channel, message, False)

	def makeReport(self, by, playerName, _type, comments):
		if playerName in self.reports["names"]:
			if not self.server.users.parsePlayerName(by) in self.reports[playerName]["reporters"]:
				self.reports[playerName]["types"].append(str(_type))
				self.reports[playerName]["reporters"].append(self.server.users.parsePlayerName(by))
				self.reports[playerName]["comments"].append(comments)
		else:
			self.reports["names"].append(playerName)
			self.reports[playerName] = {}
			self.reports[playerName]["types"] = [str(_type)]
			self.reports[playerName]["reporters"] = [self.server.users.parsePlayerName(by)]
			self.reports[playerName]["comments"] = [comments]
			self.reports[playerName]["status"] = "online" if playerName in self.server.users.players else "disconnected"
			self.reports[playerName]["langue"] = by.langue.lower()
			self.sendAllMessage("{} reported {} ({}).".format(self.server.users.parsePlayerName(by), playerName, "Hack" if _type == 0 else "Spam/Flood" if _type == 1 else "Insults" if _type == 2 else "Pishing" if _type == 3 else "Other"))

		self.updateModoPwet()
		
	def openModoPwet(self, player):
		reports = 0
		totalReports = len(self.reports["names"])
		count = 0

		bannedList = {}
		deletedList = {}
		disconnectList = []

		p = ByteArray()

		while reports < totalReports:
			playerName = self.reports["names"][reports]
			reports += 1
				
			if player.modoPwetLangue == "ALL" or self.reports[playerName]["langue"] == player.modoPwetLangue.upper():
				count += 1
				if count >= 255:
					break

				p.writeUnsignedByte(count)
				p.writeShort(reports)
				p.writeUTF(self.reports[playerName]["langue"].upper())
				p.writeUTF(playerName)
				roomName = self.getPlayerRoomName(playerName)
				p.writeUTF(roomName)
				mods = self.getModsRoom(roomName)
				p.writeByte(len(mods))
				for mod in mods:
					p.writeUTF(mod)
				p.writeInt(self.getProfileCheeseCount(playerName))

				reporters = 0
				totalReporters = len(self.reports[playerName]["types"])
				p.writeByte(totalReporters)

				while reporters < totalReporters:
					reporters += 1
					p.writeUTF(self.reports[playerName]["reporters"][reporters - 1])
					p.writeShort(self.getProfileCheeseCount(self.reports[playerName]["reporters"][reporters - 1]))
					p.writeUTF(self.reports[playerName]["comments"][reporters - 1])
					p.writeByte(self.reports[playerName]["types"][reporters - 1])
					p.writeShort(reporters)

				p.writeBoolean(playerName in list(self.server.mutes))
				if playerName in list(self.server.mutes):
					mute = self.server.mutes[playerName]
					p.writeUTF(mute["by"])
					p.writeShort(self.server.getHoursDiff(mute["time"]))
					p.writeUTF(mute["reason"])

				if self.reports[playerName]["status"] == "banned":
					x = {}
					x["banhours"] = self.reports[playerName]["banhours"]
					x["banreason"] = self.reports[playerName]["banreason"]
					x["bannedby"] = self.reports[playerName]["bannedby"]
					bannedList[playerName] = x

				if self.reports[playerName]["status"] == "deleted":
					x = {}
					x["deletedby"] = self.reports[playerName]["deletedby"]
					deletedList[playerName] = x

				if self.reports[playerName]["status"] == "disconnected":
					disconnectList.append(playerName)

			self.server.users.sendPacket(player.channel, [25, 2], ByteArray().writeUnsignedByte(count).writeBytes(p.toByteArray()).toByteArray())

			for user in disconnectList:
				self.changeReportStatusDisconnect(player, user)

			for user in deletedList.keys():
				self.changeReportStatusDeleted(player, user, deletedList[user]["deletedby"])

			for user in bannedList.keys():
				self.changeReportStatusBanned(player, user, bannedList[user]["banhours"], bannedList[user]["banreason"], bannedList[user]["bannedby"])

	def changeReportStatusDisconnect(self, player, playerName):
		self.server.users.sendPacket(player.channel, [25, 6], ByteArray().writeUTF(playerName).toByteArray())

	def changeReportStatusDeleted(self, player, playerName, deletedby):
		self.server.users.sendPacket(player.channel, [25, 7], ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

	def changeReportStatusBanned(self, player, playerName, banhours, banreason, bannedby):
		self.server.users.sendPacket(player.channel, [25, 5], ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

	def sendChatLog(self, player, player2):
		packet = ByteArray()
		packet.writeUTF(self.server.users.parsePlayerName(player2))
		packet.writeByte(len(list(player2.chatLog["room"])))
		for message in player2.chatLog["room"]:
			packet.writeUTF(message)
			packet.writeUTF("")
		packet.writeByte(len(list(player2.chatLog["whisper"])))
		for playerName, messages in player2.chatLog["whisper"].items():
			packet.writeUTF(playerName)
			packet.writeByte(len(messages))
			for message in messages:
				packet.writeUTF(message)
				packet.writeUTF("")
		self.server.users.sendPacket(player.channel, [25, 10], packet.toByteArray())