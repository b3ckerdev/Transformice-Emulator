class ScreenEvents:
	C, CC = 29, 21

	@staticmethod
	def parse(users, channel, packet, packetID):
		textAreaID = packet.readInt()
		textAreaText = packet.readUTF()

		if textAreaText == "openSeasonMessage":
			users.sendSeasonRanking(channel)
			users.sendRemoveTextArea(channel, 41)
		elif textAreaText == "closeSeasonMessage":
			for i in range(40):
				users.sendRemoveTextArea(channel, i+1)
			users.sendAddTextArea(channel, 41, "<br><p align='center'><N><a href='event:openSeasonMessage'><B>Ranking da Temporada</B></a></N></p>", 620, 13, 175, 35, int("324650", 16), 0, 100)
