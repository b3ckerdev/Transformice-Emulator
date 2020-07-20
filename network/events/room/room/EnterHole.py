class EnterHole:
	C, CC = 5, 18

	@staticmethod
	def parse(users, channel, packet, packetID):
		holeType = packet.readByte()
		codePartie = packet.readInt()
		monde = packet.readInt()
		distance = packet.readShort()
		holeX = packet.readShort()
		holeY = packet.readShort()

		player = channel.player
		room = player.room

		users.playerWin(player, holeType, codePartie, monde, distance, holeX, holeY)