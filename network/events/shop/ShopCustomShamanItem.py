class ShopCustomShamanItem:
	C, CC = 20, 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readShort()
		length = packet.readByte()
		customs = []

		player = channel.player

		for i in range(length):
			customs.append(packet.readInt())

		for item in player.shamanItems:
			if "_" in item:
				itemSplit = item.split("_")
				if itemSplit[0] == str(fullItem):
					customsColors = map(lambda color: "%06X" %(0xffffff & color), customs)
					itemSplit[1] = "+".join(customsColors)
					player.shamanItems.remove(item)

					itemStr = str(fullItem)
					itemCat = int(itemStr[len(itemStr)-2:])
					index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
					index -= 1

					player.shamanItems.append("{}_{}".format(itemSplit[0], itemSplit[1]))

					lookItems = player.shamanLook.split(",")

					if "_" in lookItems[index]:
						if lookItems[index].split("_")[0] == itemStr:
							lookItems[index] = "{}_{}".format(itemStr, itemSplit[1])

							player.lookItems = ",".join(lookItems)
					break

		users.shop.sendShopList(player)
		users.shop.sendShamanLook(player)