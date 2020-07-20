from network.packet.ByteArray import *

class ProjectionSkill:
	C, CC = 5, 16

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [5, 16], ByteArray().writeBytes(packet.toByteArray()).toByteArray())