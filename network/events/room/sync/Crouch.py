from network.packet.ByteArray import *

class Crouch:
	C, CC = 4, 9

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.server.rooms.sendAllOthers(channel.player, channel.player.room, [4, 9], ByteArray().writeInt(channel.player.playerCode).writeByte(packet.readByte()).writeByte(0).toByteArray())