class ShopEquip:
	C, CC = 20, 18

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readInt()
		x = users.shop.getCatByItem(fullItem)
		item = x[0]
		cat = x[1]

		player = channel.player

		lookSplit = player.playerLook.split(";")
		lookItems = lookSplit[1].split(",")

		if cat == 21:
			lookSplit[0] = "1"
			color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
			player.mouseColor = "78583a" if player.mouseColor == color else color
		elif cat == 22:
			if str(lookSplit[0]) == str(item):
				lookSplit[0] = "1"
			else:
				lookSplit[0] = str(item)
		else:
			if "_" in lookItems[cat]:
				c_ID = lookItems[cat].split("_")[0]
				if str(c_ID) == str(item):
					lookItems[cat] = "0"
				else:
					lookItems[cat] = "{}{}".format(item, users.shop.getItemCustomization(player, fullItem, False))
			else:
				if lookItems[cat] == str(item):
					lookItems[cat] = "0"
				else:
					lookItems[cat] = "{}{}".format(item, users.shop.getItemCustomization(player, fullItem, False))
			player.mouseColor = "78583a"

		player.playerLook = "{};{}".format(lookSplit[0], ",".join(lookItems))
		users.shop.sendLookChange(player)