from network.packet.ByteArray import *

class ConvertSkill:
	C, CC = 5, 14

	@staticmethod
	def parse(users, channel, packet, packetID):
		objectID = packet.readInt()
		users.server.rooms.sendAll(channel.player.room, [5, 13], ByteArray().writeInt(objectID).writeByte(0).toByteArray())