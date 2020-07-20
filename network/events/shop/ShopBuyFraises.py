class ShopBuyFraises:
	C, CC = 12, 10

	@staticmethod
	def parse(users, channel, packet, packetID):
		paymentMethod = packet.readByte()
		return