from network.packet.ByteArray import *

class IgnoredsAdd:
	code = 42

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()

		player = channel.player

		if not users.checkPlayerNameExist(playerName):
			users.server.tribulle.sendTribullePacket(channel.player, 43, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
		elif len(player.ignoredsList) >= 200:
			users.server.tribulle.sendTribullePacket(channel.player, 43, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
		elif playerName in player.friendsList:
			users.server.tribulle.sendTribullePacket(channel.player, 43, ByteArray().writeInt(tribulleID).writeByte(4).toByteArray())
		elif playerName in player.ignoredsList:
			users.server.tribulle.sendTribullePacket(channel.player, 43, ByteArray().writeInt(tribulleID).writeByte(4).toByteArray())
		else:
			player.ignoredsList.append(playerName)

			users.server.tribulle.sendTribullePacket(channel.player, 43, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())