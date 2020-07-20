from network.packet.ByteArray import *

class IgnoredsRemove:
	code = 44

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()

		player = channel.player

		if not playerName in player.ignoredsList:
			users.server.tribulle.sendTribullePacket(channel.player, 45, ByteArray().writeInt(tribulleID).writeByte(0).toByteArray())
		else:
			player.ignoredsList.remove(playerName)

			users.server.tribulle.sendTribullePacket(channel.player, 45, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
