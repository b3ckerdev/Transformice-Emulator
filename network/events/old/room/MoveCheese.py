class MoveCheese:
	C, CC = 5, 16

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [5, 16], values)