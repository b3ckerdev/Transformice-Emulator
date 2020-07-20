class ModopwetDelete:
	C, CC = 25, 23

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		playerName = packet.readUTF()
		closeType = packet.readByte()

		if player.privLevel >= 5:
			if playerName in users.server.modopwet.reports:
				users.server.modopwet.reports[playerName]["status"] = "deleted"
				users.server.modopwet.reports[playerName]["deletedby"] = users.parsePlayerName(player)
			users.server.modopwet.updateModoPwet()