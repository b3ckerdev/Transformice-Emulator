class DrawPoints:
	C, CC = 25, 5

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOthersOld(player, room, [25, 5], values)