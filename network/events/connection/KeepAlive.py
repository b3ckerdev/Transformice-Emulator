class KeepAlive:
	C, CC = 26, 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		channel.lastDummyTime = users.server.getTime()