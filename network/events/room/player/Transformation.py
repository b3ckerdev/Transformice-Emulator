from network.packet.ByteArray import *

class Transformation:
	C, CC = 27, 11

	@staticmethod
	def parse(users, channel, packet, packetID):
		objectID = packet.readShort()

		player = channel.player

		if not player.isDead:
			users.server.rooms.sendAll(channel.player.room, [27, 11], ByteArray().writeInt(player.playerCode).writeShort(objectID).toByteArray())