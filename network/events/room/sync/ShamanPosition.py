from network.packet.ByteArray import *

class ShamanPosition:
	C, CC = 4, 8

	@staticmethod
	def parse(users, channel, packet, packetID):
		if channel.player.isShaman:
			users.server.rooms.sendAll(channel.player.room, [4, 10], ByteArray().writeInt(channel.player.playerCode).writeBytes(packet.toByteArray()).toByteArray())