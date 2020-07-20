class ShopBuyCustomItem:
	C, CC = 20, 20

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readInt()
		isFraise = packet.readBoolean()
		price = 20 if isFraise else 2000
		x = users.shop.getCatByItem(fullItem)

		player = channel.player

		if isFraise:
			if player.shopFraises < price:
				return
			else:
				player.shopFraises -= price
		else:
			if player.shopCheeses < price:
				return
			else:
				player.shopCheeses -= price

		items = player.shopItems

		for shopItem in items:
			item = shopItem.split("_")[0] if "_" in shopItem else shopItem
			if fullItem == int(item):
				items[items.index(shopItem)] = shopItem + "_"
				break

		lookSplit = player.playerLook.split(";")
		lookItems = lookSplit[1].split(",")

		if lookItems[x[1]] == str(x[0]):
			lookItems[x[1]] = "{}_".format(x[0])

		player.playerLook = "{};{}".format(lookSplit[0], ",".join(lookItems))
		
		player.shopItems = items
		users.shop.sendShopList(player)