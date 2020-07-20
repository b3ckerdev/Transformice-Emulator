class ModopwetFollow:
	C, CC = 25, 24

	@staticmethod
	def parse(users, channel, packet, packetID):
		playerName = packet.readUTF()
		isHide = packet.readBoolean()

		player = channel.player

		if player.privLevel >= 5 and playerName in users.players:
			player.isHide = isHide

			users.server.modopwet.followPlayer(player, playerName)