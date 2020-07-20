class EditeurExit:
	C, CC = 14, 26

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player

		users.enterRoom(player, users.server.rooms.getRecommendRoom(users.server.langues.getLangue(player.langueID), "1"))