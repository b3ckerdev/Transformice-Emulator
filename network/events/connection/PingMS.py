class PingMS:
	C, CC = 26, 25

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.sendPacket(channel, [26, 25], b"")