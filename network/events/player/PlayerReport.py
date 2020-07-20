class PlayerReport:
	C, CC = 8, 25

	@staticmethod
	def parse(users, channel, packet, packetID):
		playerName = packet.readUTF().capitalize()
		reportType = packet.readByte()
		comment = packet.readUTF()

		player = channel.player
		room = channel.player.room

		if playerName == users.parsePlayerName(player):
			users.sendOldPacket(channel, [26, 9], ["0"])
		elif playerName in users.players:
			if users.players[playerName].privLevel < 5:
				users.server.modopwet.makeReport(player, playerName, reportType, comment)
			users.sendOldPacket(channel, [26, 9], ["0"])
		else:
			users.sendOldPacket(channel, [26, 9], [])