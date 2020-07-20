class ModopwetLangue:
	C, CC = 25, 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		langue = packet.readUTF()

		player = channel.player

		if player.privLevel >= 7:
			player.modoPwetLangue = langue.upper()