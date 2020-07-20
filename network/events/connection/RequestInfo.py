from network.packet.ByteArray import *

class RequestInfo:
	C, CC = 28, 50

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.sendPacket(channel, [28, 50], ByteArray().writeUTF("http://51.158.113.197/info.php").toByteArray())