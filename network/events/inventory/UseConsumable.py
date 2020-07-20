class UseConsumable:
	C, CC = 31, 3

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		consumable = packet.readShort()

		users.inventory.useConsumable(player, consumable)