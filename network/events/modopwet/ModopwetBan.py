class ModopwetBan:
	C, CC = 25, 25

	@staticmethod
	def parse(users, channel, packet, packetID):
		playerName = packet.readUTF()
		iban = packet.readBoolean()

		player = channel.player

		if player.privLevel >= 5 and playerName in users.players:
			command = "iban {} 360 Hack".format(playerName) if iban else "ban {} 360 Hack".format(playerName)
			users.commands.parse(channel, command)