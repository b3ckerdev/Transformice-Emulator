class Tribulle:
	C, CC = 60, 3

	@staticmethod
	def parse(users, channel, packet, packetID):
		code = packet.readShort()

		if code in users.packetManage.tribullePackets:
			users.packetManage.tribullePackets[code].parse(users, channel, packet, packetID)
		else:
			users.server.println("[{}] Tribulle Packet not Found: code: {} - packet: {}".format(channel.ipAddress, code, repr(packet.toByteArray())), "debug")