class ChatLog:
	C, CC = 25, 27

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		if player.privLevel >= 5:
			playerName = packet.readUTF().capitalize()

			if playerName in list(users.players):
				users.server.modopwet.sendChatLog(player, users.players[playerName])
			else:
				users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))