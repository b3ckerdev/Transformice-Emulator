from network.packet.ByteArray import *

class OldProtocol:
	C, CC = 1, 1

	@staticmethod
	def parse(users, channel, packet, packetID):
		_packet = packet.readUTF()
		values = _packet.split("\x01")
		C = ord(values[0][0])
		CC = ord(values[0][1])
		values = values[1:]

		if (C << 8 | CC) in users.packetManage.oldPackets:
			users.packetManage.oldPackets[(C << 8 | CC)].parse(users, channel, values, packetID)
		else:
			users.server.println("[{}] Packet not Found: Old C: {} - Old CC: {} - values: {}".format(channel.ipAddress, C, CC, values), "debug")