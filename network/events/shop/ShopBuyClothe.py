class ShopBuyClothe:
	C, CC = 20, 22

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		clotheID = packet.readByte()
		isFraise = packet.readBoolean()

		if isFraise:
			price = 5 if clotheID == 0 else 50 if clotheID == 1 else 100

			if player.shopFraises < price:
				return

			player.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
		else:
			price = 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

			if player.shopCheeses < price:
				return

			player.shopCheeses -= price

		player.clothes.append("%02d/%s/%s/%s" % (clotheID, "1;0,0,0,0,0,0,0,0,0,0,0", "78583a", "fade55" if player.shamanSaves >= 1000 else "95d9d6"))
		users.shop.sendShopList(player)