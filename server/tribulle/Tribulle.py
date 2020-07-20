from server.helpers.String import *
from network.packet.ByteArray import *

class TribulleServer:
	def __init__(self, server, users):
		self.server = server
		self.users = users

	def getPlayerOnlineData(self, player, player2):
		return ByteArray().writeInt(player2.playerID).writeUTF(self.users.parsePlayerName(player2).lower()).writeByte(player2.gender).writeInt(player2.playerID).writeBoolean(self.users.parsePlayerName(player) in player2.friendsList).writeBoolean(True).writeInt(4).writeUTF(player2.room.roomName).writeInt(0).toByteArray()

	def getPlayerDBData(self, player, pool_result):
		return ByteArray().writeInt(pool_result["playerID"]).writeUTF("{}#{}".format(pool_result["playerName"], pool_result["playerTag"]).lower()).writeByte(pool_result["gender"]).writeInt(pool_result["playerID"]).writeBoolean(self.users.parsePlayerName(player) in pool_result["friendsList"].split(",")).writeBoolean(False).writeInt(1).writeUTF("").writeInt(pool_result["lastLogin"]).toByteArray()

	def getPlayerNoData(self):
		return ByteArray().writeInt(0).writeUTF("").writeByte(0).writeInt(0).writeBoolean(False).writeBoolean(False).writeInt(1).writeUTF("").writeInt(0).toByteArray()

	def getFriendsClass(self, player):
		c = []
		for friend in player.friendsList:
			if friend in self.users.players:
				c.append(self.users.players[friend])
		return c

	def sendTribullePacket(self, player, code, data):
		self.users.sendPacket(player.channel, [60, 3], ByteArray().writeShort(code).writeBytes(data).toByteArray())

	def joinTribulle(self, player):
		self.users.sendPacket(player.channel, [60, 4], ByteArray().writeBoolean(True).toByteArray())

		p = ByteArray().writeByte(player.gender).writeInt(player.playerID)

		if player.marriage in self.users.players:
			marriage = self.users.players[player.marriage]
			p.writeBytes(self.getPlayerOnlineData(player, marriage))
		elif self.users.checkPlayerNameExist(player.marriage):
			name, tag = player.marriage.split("#")
			pool = self.server.database.execute("SELECT * FROM users WHERE playerName = %s AND playerTag = %s", (name, tag))
			results = self.server.database.fetchone(pool)
			p.writeBytes(self.getPlayerDBData(player, results))
		else:
			p.writeBytes(self.getPlayerNoData())

		p.writeShort(len(player.friendsList))
		for friend in player.friendsList:
			if friend in self.users.players:
				f = self.users.players[friend]
				p.writeBytes(self.getPlayerOnlineData(player, f))
			elif self.users.checkPlayerNameExist(friend):
				name, tag = friend.split("#")
				pool = self.server.database.execute("SELECT * FROM users WHERE playerName = %s AND playerTag = %s", (name, tag))
				results = self.server.database.fetchone(pool)
				p.writeBytes(self.getPlayerDBData(player, results))
			else:
				p.writeBytes(self.getPlayerNoData())

		p.writeShort(len(player.ignoredsList))
		for ignored in player.ignoredsList:
			p.writeUTF(ignored)

		if player.tribe != None:
			p.writeUTF(self.session.tribe.tribeName).writeInt(self.session.tribe.tribeID).writeUTF(self.session.tribe.tribeMessage).writeInt(self.session.tribe.tribeHouse).writeUTF(self.session.tribe.tribeRanks).writeInt(self.session.user["tribe_rank"])
		else:
			p.writeUTF("").writeInt(0).writeUTF("").writeInt(0).writeUTF("").writeInt(0)

		self.sendTribullePacket(player, 3, p.toByteArray())

		for friend in self.getFriendsClass(player):
			self.server.tribulle.sendFriendConnected(player, friend)

	def sendFriendsList(self, player):
		p = ByteArray()
		if player.marriage in self.users.players:
			marriage = self.users.players[player.marriage]
			p.writeBytes(self.getPlayerOnlineData(player, marriage))
		elif self.users.checkPlayerNameExist(player.marriage):
			name, tag = player.marriage.split("#")
			pool = self.server.database.execute("SELECT * FROM users WHERE playerName = %s AND playerTag = %s", (name, tag))
			results = self.server.database.fetchone(pool)
			p.writeBytes(self.getPlayerDBData(player, results))
		else:
			p.writeBytes(self.getPlayerNoData())

		p.writeShort(len(player.friendsList))
		for friend in player.friendsList:
			if friend in self.users.players:
				f = self.users.players[friend]
				p.writeBytes(self.getPlayerOnlineData(player, f))
			elif self.users.checkPlayerNameExist(friend):
				name, tag = friend.split("#")
				pool = self.server.database.execute("SELECT * FROM users WHERE playerName = %s AND playerTag = %s", (name, tag))
				results = self.server.database.fetchone(pool)
				p.writeBytes(self.getPlayerDBData(player, results))
			else:
				p.writeBytes(self.getPlayerNoData())

		self.sendTribullePacket(player, 34, p.toByteArray())

	def sendIgnoredsList(self, player, tribulleID):
		p = ByteArray()
		p.writeInt(tribulleID)
		p.writeShort(len(player.ignoredsList))
		for ignored in player.ignoredsList:
			p.writeUTF(ignored)
		self.sendTribullePacket(player, 47, p.toByteArray())

	def sendFriendConnected(self, player, player2):
		self.sendTribullePacket(player2, 32, ByteArray().writeUTF(self.users.parsePlayerName(player).lower()).toByteArray())

	def sendFriendDisconnected(self, player, player2):
		self.sendTribullePacket(player2, 33, ByteArray().writeUTF(self.users.parsePlayerName(player).lower()).toByteArray())
		self.sendTribullePacket(player2, 35, ByteArray().writeInt(player.playerID).writeUTF(self.users.parsePlayerName(player).lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(0).writeInt(1).writeUTF("").writeInt(player.lastLogin).toByteArray())

	def sendFriendChangedRoom(self, player, player2):
		self.sendTribullePacket(player2, 35, ByteArray().writeInt(player.playerID).writeUTF(self.users.parsePlayerName(player).lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(4).writeUTF(player.room.roomName).writeInt(0).toByteArray())

	def sendChatJoin(self, player, chatName):
		self.sendTribullePacket(player, 62, ByteArray().writeUTF(chatName).toByteArray())

	def sendChatQuem(self, player, tribulleID, chatName):
		quem = self.server.chats[chatName] if chatName in self.server.chats else []
		p = ByteArray().writeInt(tribulleID).writeByte(len(quem) > 0).writeShort(len(quem))
		for playerName in quem:
			p.writeUTF(playerName)
		self.sendTribullePacket(player, 59, p.toByteArray())