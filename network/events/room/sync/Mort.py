class Mort:
	C, CC = 4, 5

	@staticmethod
	def parse(users, channel, packet, packetID):
		codePartie = packet.readInt()
		player = channel.player
		room = player.room

		if codePartie == room.lastCodePartie:
			users.sendPlayerDied(player)

		if not room.noShamanSkills:
			if room.bubblesCount > 0:
				if room.rooms.getAliveCount(room) != 1:
					room.bubblesCount -= 1
					users.sendPlaceObject(player, room, room.lastObjectID + 2, 59, player.posX, 450, 0, 0, 0, True, True)

			if player.desintegration:
				users.skills.sendSkillObject(room, 6, player.posX, 395, 0)