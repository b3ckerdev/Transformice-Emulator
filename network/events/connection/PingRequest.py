class PingRequest:
	C, CC = 28, 6

	@staticmethod
	def parse(users, channel, packet, packetID):
		pingID = packet.readByte()

		if pingID == 20:
			channel.player.playerPing[1] = int(round(users.server.getTime() * 1000) - channel.player.playerPing[0])
			channel.lastPingTime = users.server.getTime()