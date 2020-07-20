class ShopEquipClothe:
	C, CC = 20, 6

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		clotheID = packet.readByte()

		for clothe in player.clothes:
			values = clothe.split("/")
			if values[0] == "%02d" % (clotheID):
				player.playerLook = values[1]
				player.mouseColor = values[2]
				player.shamanColor = values[3]
				break

		users.shop.sendLookChange(player)
		users.shop.sendShopList(player)