class EquipConsumable:
	C, CC = 31, 4

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		consumable = packet.readShort()

		users.inventory.equipConsumable(player, consumable)