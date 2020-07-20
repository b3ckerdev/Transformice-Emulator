from network.packet.ByteArray import *

class ShopBuyShamanItem:
	C, CC = 20, 23

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readShort()
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

		player.shamanItems.append(str(fullItem))
		users.shop.sendShopList(player)
		users.checkShopTitleUnlocked(player)
		users.sendPacket(channel, [20, 2], ByteArray().writeInt(fullItem).writeByte(0).toByteArray())
		users.server.rooms.sendAll(player.room, [8, 44], ByteArray().writeInt(player.playerCode).writeByte(1).writeInt(fullItem).toByteArray())
