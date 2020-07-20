class PacketError:
	C, CC = 28, 4

	@staticmethod
	def parse(users, channel, packet, packetID):
		Token = [packet.readByte(), packet.readByte()]
		oldToken = [packet.readByte(), packet.readByte()]
		message = packet.readUTF()

		if Token != [0, 0]:
			users.server.println("[{}] Packet Error: C: {} - CC: {} - Message: {}".format(channel.ipAddress, Token[0], Token[1], message), "debug")
		else:
			users.server.println("[{}] Packet Error: Old C: {} - Old CC: {} - Message: {}".format(channel.ipAddress, oldToken[0], oldToken[1], message), "debug")