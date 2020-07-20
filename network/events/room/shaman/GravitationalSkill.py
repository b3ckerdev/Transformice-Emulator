from network.packet.ByteArray import *

class GravitationalSkill:
	C, CC = 5, 28

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAll(channel.player.room, [5, 28], ByteArray().writeShort(0).writeBytes(packet.toByteArray()).toByteArray())