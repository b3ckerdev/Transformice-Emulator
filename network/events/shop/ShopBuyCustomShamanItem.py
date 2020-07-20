class ShopBuyCustomShamanItem:
	C, CC = 20, 25

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readShort()
		isFraise = packet.readBoolean()
		price = 150 if isFraise else 4000
		x = users.shop.getCatByShaman(fullItem)

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

		items = player.shamanItems

		for shopItem in items:
			item = shopItem.split("_")[0] if "_" in shopItem else shopItem
			if fullItem == int(item):
				items[items.index(shopItem)] = shopItem + "_"
				break

		shamanLookSplit = player.shamanLook.split(",")

		if shamanLookSplit[x[1]] == str(fullItem):
			shamanLookSplit[x[1]] = "{}_".format(fullItem)

		player.shamanLook = ",".join(shamanLookSplit)
		
		player.shamanItems = items
		users.shop.sendShopList(player)