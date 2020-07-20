from network.packet.ByteArray import *

class DemolitionSkill:
	C, CC = 5, 15

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [5, 15], ByteArray().writeBytes(packet.toByteArray()).toByteArray())