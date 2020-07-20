from network.packet.ByteArray import *

class RemoveInvocation:
	C, CC = 100, 3

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [100, 3], ByteArray().writeInt(channel.player.playerCode).toByteArray())