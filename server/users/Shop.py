from network.packet.ByteArray import *

class Shop:
	def __init__(self, users):
		self.users = users
		self.server = users.server
		
	def getCatByItem(self, item):
		x = [0] * 2
		fl = 0
		if item > 230000:
			fl = 22
			item = item - 230000
		elif item > 33000:
			fl = 22
			item = item - 33392
		elif item > 10000:
			fl = 0
			item = item - 10000
		else:
			fl = item / 100
			item = item % 100
		x[0] = item
		x[1] = int(fl)
		return x

	def getCatByShaman(self, item):
		sitem = str(item)
		cat = int(sitem[:len(sitem)-2])
		index = cat if cat <= 4 else cat - 1 if cat <= 7 else 7 if cat == 10 else 8 if cat == 17 else 9
		index -= 1
		return [item, index]

	def getItemCustomization(self, player, checkItem, isShamanShop):
		items = player.shamanItems if isShamanShop else player.shopItems
		for item in items:
			if "_" in item:
				if int(item.split("_")[0]) == int(checkItem):
					return "_{}".format(item.split("_")[1])
			else:
				if int(item) == int(checkItem):
					break
		return ""

	def sendShopList(self, player):
		p = ByteArray().writeInt(player.shopCheeses).writeInt(player.shopFraises).writeUTF(player.playerLook).writeInt(len(player.shopItems))
		for item in player.shopItems:
			if "_" in item:
				itemSplited = item.split("_")
				realItem = itemSplited[0]
				custom = itemSplited[1] if len(itemSplited) >= 2 else ""
				realCustom = [] if custom == "" else custom.split("+")
				p.writeByte(len(realCustom)+1).writeInt(int(realItem))
				for cust in realCustom:
					p.writeInt(int(cust, 16))
			else:
				p.writeByte(0).writeInt(int(item))
		p.writeInt(0).writeByte(0).writeShort(len(player.clothes))
		for clothe in player.clothes:
			clotheSplited = clothe.split("/")
			p.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])
		p.writeShort(len(player.shamanItems))
		for item in player.shamanItems:
			if "_" in item:
				itemSplited = item.split("_")
				realItem = itemSplited[0]
				custom = itemSplited[1] if len(itemSplited) >= 2 else ""
				realCustom = [] if custom == "" else custom.split("+")
				p.writeShort(int(realItem)).writeBoolean(item in player.shamanLook.split(",")).writeByte(len(realCustom)+1)
				for cust in realCustom:
					p.writeInt(int(cust, 16))
			else:
				p.writeShort(int(item)).writeBoolean(item in player.shamanLook.split(",")).writeByte(0)
		p.writeShort(0)
		self.users.sendPacket(player.channel, [8, 20], p.toByteArray())

	def sendLookChange(self, player):
		p = ByteArray()
		look = player.playerLook.split(";")
		p.writeShort(int(look[0]))
		for item in look[1].split(","):
			if "_" in item:
				itemSplited = item.split("_")
				realItem = itemSplited[0]
				custom = itemSplited[1] if len(itemSplited) >= 2 else ""
				realCustom = [] if custom == "" else custom.split("+")
				p.writeInt(int(realItem)).writeByte(len(realCustom))
				for cust in realCustom:
					p.writeInt(int(cust, 16))
			else:
				p.writeInt(int(item)).writeByte(0)
		p.writeInt(int(player.mouseColor, 16))
		self.users.sendPacket(player.channel, [20, 17], p.toByteArray())

	def sendShamanLook(self, player):
		p = ByteArray()
		count = 0
		for item in player.shamanLook.split(","):
			realItem = int(item.split("_")[0]) if "_" in item else int(item)
			if realItem != 0:
				p.writeShort(realItem)
				count += 1
		self.users.sendPacket(player.channel, [20, 24], ByteArray().writeShort(count).writeBytes(p.toByteArray()).toByteArray())

	def sendShamanItems(self, player):
		p = ByteArray()
        
		shamanItems = player.shamanItems
		p.writeShort(len(shamanItems))

		for item in shamanItems:
			if "_" in item:
				itemSplited = item.split("_")
				realItem = itemSplited[0]
				custom = itemSplited[1] if len(itemSplited) >= 2 else ""
				realCustom = [] if custom == "" else custom.split("+")
				p.writeShort(int(realItem)).writeBoolean(item in player.shamanLook.split(",")).writeByte(len(realCustom)+1)
				x = 0
				while x < len(realCustom):
					p.writeInt(int(realCustom[x], 16))
					x += 1
			else:
				p.writeShort(int(item)).writeBoolean(item in player.shamanLook.split(",")).writeByte(0)
                        
		self.users.sendPacket(player.channel, [20, 27], p.toByteArray())

	def getShamanItemCustom(self, player, code):
		item = player.shamanItems
		for item in player.shamanItems:
			if "_" in item:
				itemSplited = item.split("_")
				custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
				custom = list(filter(str, custom))
				if int(itemSplited[0]) == code:
					p = ByteArray().writeByte(len(custom))
					x = 0
					while x < len(custom):
						p.writeInt(int(custom[x], 16))
						x += 1
					return p.toByteArray()
		return b"\x00"