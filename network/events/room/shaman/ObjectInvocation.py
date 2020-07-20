from network.packet.ByteArray import *

class ObjectInvocation:
	C, CC = 100, 2

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [100, 2], ByteArray().writeInt(channel.player.playerCode).writeBytes(packet.toByteArray()).toByteArray())