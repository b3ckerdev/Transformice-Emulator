class ShamanFly:
	C, CC = 8, 15

	@staticmethod
	def parse(users, channel, packet, packetID):
		fly = packet.readBoolean()

		users.skills.sendShamanFly(channel.player, fly)