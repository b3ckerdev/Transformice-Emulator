class Points:
	C, CC = 5, 25

	@staticmethod
	def parse(users, channel, packet, packetID):
		if users.server.rooms.getPlayersCount(channel.player.room) >= 2:
			channel.player.playerScore += 1