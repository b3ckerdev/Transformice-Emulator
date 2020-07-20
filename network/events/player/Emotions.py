from network.packet.ByteArray import *

class Emotions:
	C, CC = 8, 5

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = channel.player.room

		room.rooms.sendAllOthers(player, room, [8, 5], ByteArray().writeInt(player.playerCode).writeBytes(packet.toByteArray()).toByteArray())