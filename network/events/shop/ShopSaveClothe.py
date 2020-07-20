class ShopSaveClothe:
	C, CC = 20, 7

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		clotheID = packet.readByte()

		x = 0
		for clothe in player.clothes:
			values = clothe.split("/")
			if values[0] == "%02d" % (clotheID):
				values[1] = player.playerLook
				values[2] = player.mouseColor
				values[3] = player.shamanColor
				player.clothes[x] = "/".join(values)
				break
			x += 1

		users.shop.sendShopList(player)