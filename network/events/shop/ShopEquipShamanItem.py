from network.packet.ByteArray import *

class ShopEquipShamanItem:
	C, CC = 20, 24

	@staticmethod
	def parse(users, channel, packet, packetID):
		fullItem = packet.readInt()
		x = users.shop.getCatByShaman(fullItem)

		player = channel.player

		shamanLookSplit = player.shamanLook.split(",")

		if "_" in shamanLookSplit[x[1]]:
			itemID = int(shamanLookSplit[x[1]].split("_")[0])
			if itemID == fullItem:
				shamanLookSplit[x[1]] = "0"
			else:
				shamanLookSplit[x[1]] = "{}{}".format(fullItem, users.shop.getItemCustomization(player, fullItem, True))
		else:
			itemID = int(shamanLookSplit[x[1]])
			if itemID == fullItem:
				shamanLookSplit[x[1]] = "0"
			else:
				shamanLookSplit[x[1]] = "{}{}".format(fullItem, users.shop.getItemCustomization(player, fullItem, True))

		player.shamanLook = ",".join(shamanLookSplit)
		users.shop.sendShamanLook(player)