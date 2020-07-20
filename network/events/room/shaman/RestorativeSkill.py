from network.packet.ByteArray import *

class RestorativeSkill:
	C, CC = 5, 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		objectID = packet.readInt()
		id = packet.readInt()
		users.server.rooms.sendAll(channel.player.room, [5, 26], ByteArray().writeInt(objectID).writeInt(id).toByteArray())