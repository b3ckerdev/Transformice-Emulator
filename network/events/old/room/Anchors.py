class Anchors:
	C, CC = 5, 7

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room
		room.rooms.sendAllOld(room, [5, 7], values)
		channel.player.room.anchors.extend(values)