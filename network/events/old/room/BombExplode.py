class BombExplode:
	C, CC = 4, 6

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [4, 6], values)