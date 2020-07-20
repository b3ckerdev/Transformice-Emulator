from network.packet.ByteArray import *

class ShopBuyMouseItem:
	C, CC = 20, 19

	@staticmethod
	def parse(users, channel, packet, packetID):
		itemID = packet.readInt()
		isFraise = packet.readBoolean()
		price = packet.readShort()

		player = channel.player

		if isFraise:
			if player.shopFraises < price:
				return

			player.shopFraises -= price
		else:
			if player.shopCheeses < price:
				return
			
			player.shopCheeses -= price

		player.shopItems.append(str(itemID))
		users.shop.sendShopList(player)
		users.checkShopTitleUnlocked(player)

		# mission
		if len(player.shopItems) >= 1 and not player.missions[50][4]:
			users.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", ["32"])
			users.skills.earnExp(player, 32)
			player.missions[50][1] += 1
			player.missions[50][4] = True
			if not 550.1 in player.titlesList:
				player.titlesList.append(550.1)
				player.titleID = 550.1
				users.sendUnlockedTitle(player)
				users.sendTitleList(player)
				users.sendChangeTitle(player)

		users.sendPacket(channel, [20, 2], ByteArray().writeInt(itemID).writeByte(1).toByteArray())
		users.server.rooms.sendAll(player.room, [8, 44], ByteArray().writeInt(player.playerCode).writeByte(0).writeInt(itemID).toByteArray())

		if itemID in users.shopBadges:
			unlockedBadge = users.shopBadges[itemID]
			player.shopBadges.append(unlockedBadge)
			users.server.rooms.sendAll(player.room, [8, 42], ByteArray().writeInt(player.playerCode).writeShort(unlockedBadge).toByteArray())