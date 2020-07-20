from network.packet.ByteArray import *

class PingUpdate:
	C, CC = 8, 30

	@staticmethod
	def parse(users, channel, packet, packetID):
		pingID = packet.readByte()

		if pingID == 20:
			channel.player.playerPing[0] = round(users.server.getTime() * 1000)

			users.sendPacket(channel, [28, 6],  ByteArray().writeByte(pingID).toByteArray())