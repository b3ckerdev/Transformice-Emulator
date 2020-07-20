from network.packet.ByteArray import *

class MarriageDivorce:
	code = 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()

		player = channel.player

		if player.marriage in users.players:
			player2 = users.players[player.marriage]

			player.marriage = ""
			player2.marriage = ""

			users.server.tribulle.sendTribullePacket(player, 41, ByteArray().writeUTF(users.parsePlayerName(player2).lower().lower()).writeBoolean(False).toByteArray())
			users.server.tribulle.sendTribullePacket(player2, 41, ByteArray().writeUTF(users.parsePlayerName(player).lower().lower()).writeBoolean(False).toByteArray())
			
			if player.friendsOpen:
				users.server.tribulle.sendFriendsList(player)

			if player2.friendsOpen:
				users.server.tribulle.sendFriendsList(player2)

			users.server.tribulle.sendTribullePacket(player, 27, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
		elif users.checkPlayerNameExist(player.marriage):
			playerName, playerTag = player.marriage.split("#")
			pool = users.server.database.execute("UPDATE users SET marriage = %s WHERE playerName = %s AND playerTag = %s", ("", playerName, playerTag))
			users.server.database.commitAll()
			
			player.marriage = ""

			if player.friendsOpen:
				users.server.tribulle.sendFriendsList(player)
				
			users.server.tribulle.sendTribullePacket(player, 27, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
		else:
			users.server.tribulle.sendTribullePacket(player, 27, ByteArray().writeInt(tribulleID).writeByte(0).toByteArray())
