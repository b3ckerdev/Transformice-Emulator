class ComputerInfo:
	C, CC = 28, 17

	@staticmethod
	def parse(users, channel, packet, packetID):
		lang = packet.readUTF()
		system = packet.readUTF()
		version = packet.readUTF()
		lByte = packet.readByte()