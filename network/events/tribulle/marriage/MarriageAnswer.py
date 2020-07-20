from network.packet.ByteArray import *

class MarriageAnswer:
	code = 24

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()
		answer = packet.readBoolean()

		player = channel.player

		if not playerName in users.players:
			users.server.tribulle.sendTribullePacket(player, 25, ByteArray().writeInt(tribulleID).writeByte(11).toByteArray())
		elif player.marriage != "":
			users.server.tribulle.sendTribullePacket(player, 25, ByteArray().writeInt(tribulleID).writeByte(11).toByteArray())
		else:
			if answer:
				player2 = users.players[playerName]
				player2.marriageInvite = ""

				player.marriage = playerName
				player2.marriage = users.parsePlayerName(player)

				users.server.tribulle.sendTribullePacket(player, 39, ByteArray().writeUTF(player.marriage.lower()).toByteArray())
				users.server.tribulle.sendTribullePacket(player2, 39, ByteArray().writeUTF(player2.marriage.lower()).toByteArray())
				
				if player.friendsOpen:
					users.server.tribulle.sendFriendsList(player)

				if player2.friendsOpen:
					users.server.tribulle.sendFriendsList(player2)

			else:
				player2 = users.players[playerName]
				player2.marriageInvite = ""
				users.server.tribulle.sendTribullePacket(player2, 40, ByteArray().writeUTF(users.parsePlayerName(player).lower()).toByteArray())

			users.server.tribulle.sendTribullePacket(player, 25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())