from network.packet.ByteArray import *

class FriendsRemove:
	code = 20

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()

		player = channel.player

		if not playerName in player.friendsList:
			users.server.tribulle.sendTribullePacket(channel.player, 21, ByteArray().writeInt(tribulleID).writeByte(0).toByteArray())
		else:
			player.friendsList.remove(playerName)

			if playerName in users.players and users.parsePlayerName(player) in users.players[playerName].friendsList and users.players[playerName].friendsOpen:
				users.server.tribulle.sendFriendsList(users.players[playerName])

			if player.friendsOpen:
				users.server.tribulle.sendFriendsList(player)

			users.server.tribulle.sendTribullePacket(channel.player, 21, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
