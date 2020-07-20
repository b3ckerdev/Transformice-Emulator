class PlaceBalloon:
	C, CC = 8, 16

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [8, 16], values)