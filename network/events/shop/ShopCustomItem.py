class ShopCustomItem:
	C, CC = 20, 21

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readInt()
		length = packet.readByte()
		customs = []
		x = users.shop.getCatByItem(fullItem)

		player = channel.player

		for i in range(length):
			customs.append(packet.readInt())

		for item in player.shopItems:
			if "_" in item:
				itemSplit = item.split("_")
				if itemSplit[0] == str(fullItem):
					customsColors = map(lambda color: "%06X" %(0xffffff & color), customs)
					itemSplit[1] = "+".join(customsColors)
					player.shopItems.remove(item)

					player.shopItems.append("{}_{}".format(itemSplit[0], itemSplit[1]))

					lookSplit = player.playerLook.split(";")
					lookItems = lookSplit[1].split(",")

					if "_" in lookItems[x[1]]:
						if lookItems[x[1]].split("_")[0] == str(x[0]):
							lookItems[x[1]] = "{}_{}".format(x[0], itemSplit[1])

							player.playerLook = "{};{}".format(lookSplit[0], ",".join(lookItems))
					break

		users.shop.sendShopList(player)