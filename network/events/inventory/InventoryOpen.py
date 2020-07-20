class InventoryOpen:
	C, CC = 31, 1

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		users.inventory.openInventory(player)