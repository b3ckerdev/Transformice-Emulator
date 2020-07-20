class ShamanMessage:
	C, CC = 5, 9

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		room.rooms.sendAll(room, [5, 9], packet.toByteArray())