from network.packet.ByteArray import *

class ShopInfos:
	C, CC = 20, 15

	@staticmethod
	def parse(users, channel, packet, packetID):
		users.sendPacket(channel, [20, 15], ByteArray().writeInt(channel.player.shopCheeses).writeInt(channel.player.shopFraises).toByteArray())