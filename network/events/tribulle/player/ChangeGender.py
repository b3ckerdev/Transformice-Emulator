from network.packet.ByteArray import *

class ChangeGender:
	code = 10

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		gender = packet.readByte()

		player = channel.player

		player.gender = gender

		users.server.tribulle.sendTribullePacket(channel.player, 12, ByteArray().writeByte(player.gender).toByteArray())
		users.server.tribulle.sendTribullePacket(channel.player, 11, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())