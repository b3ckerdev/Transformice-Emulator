from network.packet.ByteArray import *

class Meep:
	C, CC = 8, 39

	@staticmethod
	def parse(users, channel, packet, packetID):
		posX = packet.readShort()
		posY = packet.readShort()

		player = channel.player

		users.server.rooms.sendAll(channel.player.room, [8, 38], ByteArray().writeInt(player.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if player.isShaman else 5).toByteArray())