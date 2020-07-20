from network.packet.ByteArray import *

class RecyclingSkill:
	C, CC = 5, 27

	@staticmethod
	def parse(users, channel, packet, packetID):
		objectID = packet.readShort()
		users.server.rooms.sendAll(channel.player.room, [5, 27], ByteArray().writeShort(objectID).toByteArray())