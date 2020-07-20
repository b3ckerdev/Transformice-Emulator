class Drawing:
	C, CC = 25, 4

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOthersOld(player, room, [25, 4], values)