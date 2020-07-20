import time, traceback

class ParsePackets:
	def __init__(self, users):
		self.users = users

		self.encryptTokens = [[6, 26], [60, 3], [60, 4], [28, 20], [28, 21], [26, 7], [60, 1], [28, 25], [6, 6], [28, 24], [26, 41]]

	def parsePacket(self, channel, packet, packetID):
		try:
			tokens = [packet.readByte(), packet.readByte()]
			
			if int(self.users.server.config["debug"]):
				if tokens != [4, 4] and tokens != [4, 3]:
					self.users.server.println("[{}] Recv: C: {} - CC: {} - packet: {}".format(channel.ipAddress, tokens[0], tokens[1], repr(packet.toByteArray())), "debug")

			if tokens != [28, 1]:
				if not channel.isValidated:
					return

			if tokens in [[26, 7], [26, 8], [26, 20]]:
				if channel.player.isLogged:
					return

			if not tokens in [[28, 1], [8, 2], [28, 17], [26, 20], [26, 7], [26, 8], [26, 26]]:
				if not channel.player.isLogged:
					return
					
			if (tokens[0] << 8 | tokens[1]) in self.users.packetManage.packets:
				if tokens in self.encryptTokens:
					packet = self.users.packetManage.packetEncryption.msg(packet, packetID)
				self.users.packetManage.packets[(tokens[0] << 8 | tokens[1])].parse(self.users, channel, packet, packetID)
			else:
				self.users.server.println("[{}] Packet not Found: C: {} - CC: {} - packet: {}".format(channel.ipAddress, tokens[0], tokens[1], repr(packet.toByteArray())), "debug")
		except Exception as ERROR:
			c = open("./errors.log", "a")
			c.write("\n" + "=" * 60 + "\n- Time: {}\n- Player: {}\n- Error: \n".format(time.strftime("%d/%m/%Y - %H:%M:%S"), self.users.parsePlayerName(channel.player)))
			traceback.print_exc(file=c)
			c.close()
			self.users.server.println("A new error was encountered.", "warn")
			channel.errors += 1

			if channel.errors >= 10:
				channel.close_connection()