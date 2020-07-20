class ConjurationStart:
	C, CC = 4, 12

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room

		room.rooms.sendAllOthersOld(player, room, [4, 12], values)