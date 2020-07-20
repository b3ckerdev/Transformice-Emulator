class ConjurationEnd:
	C, CC = 4, 13

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room

		room.rooms.sendAllOthersOld(player, room, [4, 13], values)