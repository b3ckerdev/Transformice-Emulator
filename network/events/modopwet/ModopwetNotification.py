class ModopwetNotification:
	C, CC = 25, 12

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		notification = packet.readBoolean()

		if player.privLevel >= 5:
			player.modoPwetNotification = notification