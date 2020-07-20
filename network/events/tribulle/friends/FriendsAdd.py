from network.packet.ByteArray import *

class FriendsAdd:
	code = 18

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()

		player = channel.player

		if not users.checkPlayerNameExist(playerName):
			users.server.tribulle.sendTribullePacket(channel.player, 19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
		elif len(player.friendsList) >= 200:
			users.server.tribulle.sendTribullePacket(channel.player, 19, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
		elif playerName in player.friendsList:
			users.server.tribulle.sendTribullePacket(channel.player, 19, ByteArray().writeInt(tribulleID).writeByte(15).toByteArray())
		elif playerName in player.ignoredsList:
			users.server.tribulle.sendTribullePacket(channel.player, 19, ByteArray().writeInt(tribulleID).writeByte(15).toByteArray())
		else:
			player.friendsList.append(playerName)

			if playerName in users.players and users.parsePlayerName(player) in users.players[playerName].friendsList and users.players[playerName].friendsOpen:
				users.server.tribulle.sendFriendsList(users.players[playerName])

			if player.friendsOpen:
				users.server.tribulle.sendFriendsList(player)

			users.server.tribulle.sendTribullePacket(channel.player, 19, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
