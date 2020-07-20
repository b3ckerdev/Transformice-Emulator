class Modopwet:
	C, CC = 25, 2

	@staticmethod
	def parse(users, channel, packet, packetID):
		isOpen = packet.readBoolean()

		player = channel.player

		if player.privLevel >= 5:
			player.modoPwet = isOpen

			if isOpen:
				users.server.modopwet.openModoPwet(player)