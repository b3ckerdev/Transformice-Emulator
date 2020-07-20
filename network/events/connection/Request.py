class Request:
	C, CC = 26, 40

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.sendPacket(channel, [26, 40], b"")