from network.packet.ByteArray import *

class ShopList:
	C, CC = 8, 20

	@staticmethod
	def parse(users, channel, packet, packetID):
		server = channel.server
		player = channel.player
		p = ByteArray()
		p.writeInt(player.shopCheeses)
		p.writeInt(player.shopFraises)
		p.writeUTF(player.playerLook)
		p.writeInt(len(player.shopItems))
		for item in player.shopItems:
			if "_" in item:
				itemSplited = item.split("_")
				realItem = itemSplited[0]
				custom = itemSplited[1] if len(itemSplited) >= 2 else ""
				realCustom = [] if custom == "" else custom.split("+")
				p.writeByte(len(realCustom)+1)
				p.writeInt(int(realItem))
				for cust in realCustom:
					p.writeInt(int(cust, 16))
			else:
				p.writeByte(0)
				p.writeInt(int(item))
		p.writeInt(len(server.shopList["mouse"]))
		for shop in server.shopList["mouse"]:
			s = shop.split(",")
			p.writeUnsignedShort(int(s[0]))
			p.writeUnsignedShort(int(s[1]))
			p.writeByte(int(s[2]))
			p.writeBoolean(int(s[3]))
			p.writeByte(int(s[4]))
			p.writeInt(int(s[5]))
			p.writeInt(int(s[6]))
			p.writeUnsignedShort(0)
		p.writeByte(0)
		p.writeShort(len(player.clothes))
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
				p.writeShort(int(realItem))
				p.writeBoolean(item in player.shamanLook.split(","))
				p.writeByte(len(realCustom)+1)
				for cust in realCustom:
					p.writeInt(int(cust, 16))
			else:
				p.writeShort(int(item))
				p.writeBoolean(item in player.shamanLook.split(","))
				p.writeByte(0)
		p.writeShort(len(server.shopList["shaman"]))
		for shop in server.shopList["shaman"]:
			s = shop.split(",")
			p.writeInt(int(s[0]))
			p.writeByte(int(s[1]))
			p.writeBoolean(int(s[2]))
			p.writeByte(int(s[3]))
			p.writeInt(int(s[4]))
			p.writeShort(int(s[5]))
		users.sendPacket(channel, [8, 20], p.toByteArray())