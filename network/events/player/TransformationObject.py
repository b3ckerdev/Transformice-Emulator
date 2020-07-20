from network.packet.ByteArray import *

class TransformationObject:
	C, CC = 27, 11

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = channel.player.room

		room.rooms.sendAll(room, [27, 11], ByteArray().writeInt(player.playerCode).writeBytes(packet.toByteArray()).toByteArray())