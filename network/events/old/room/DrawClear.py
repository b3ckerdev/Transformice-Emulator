class DrawClear:
	C, CC = 25, 3

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [25, 3], values)