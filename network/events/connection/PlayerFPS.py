class PlayerFPS:
	C, CC = 26, 13

	@staticmethod
	def parse(users, channel, packet, packetID):
		d = packet.readShort()