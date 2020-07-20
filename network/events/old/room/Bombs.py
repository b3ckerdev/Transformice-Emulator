class Bombs:
	C, CC = 5, 17

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [5, 17], values)