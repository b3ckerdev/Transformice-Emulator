class ChangeShamanColor:
	C, CC = 28, 18

	@staticmethod
	def parse(users, channel, packet, packetID):
		color = packet.readInt()

		channel.player.shamanColor = "%06X" %(0xFFFFFF & color)