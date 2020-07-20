class ChatQuem:
	code = 58

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		chatName = packet.readUTF()

		player = channel.player

		users.server.tribulle.sendChatQuem(player, tribulleID, chatName)