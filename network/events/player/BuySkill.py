class BuySkill:
	C, CC = 8, 21

	@staticmethod
	def parse(users, channel, packet, packetID):
		skillID = packet.readByte()

		users.skills.buySkill(channel.player, skillID)