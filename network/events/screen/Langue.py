class Langue:
	C, CC = 8, 2

	@staticmethod
	def parse(users, channel, packet, packetID):
		langueID = packet.readByte()
		langue = users.server.langues.getLangue(langueID)

		channel.player.langue = langue
		channel.player.langueID = langueID

		#channel.player.langue = "BR"
		#channel.player.langueID = 3