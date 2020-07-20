from network.packet.ByteArray import *

class AntigravitySkill:
	C, CC = 5, 29

	@staticmethod
	def parse(users, channel, packet, packetID):
		objectID = packet.readInt()
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [5, 29], ByteArray().writeInt(objectID).writeShort(0).toByteArray())