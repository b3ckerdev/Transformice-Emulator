class RemoveBalloon:
	C, CC = 8, 17

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOthersOld(player, room, [8, 16], [player.playerCode, "0"])