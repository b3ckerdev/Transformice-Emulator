class ShamanType:
	C, CC = 28, 10

	@staticmethod
	def parse(users, channel, packet, packetID):
		shamanType = packet.readByte()

		channel.player.shamanType = shamanType
		users.sendShamanType(channel.player, channel.player.shamanType, True)