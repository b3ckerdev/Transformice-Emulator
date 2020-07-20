from network.packet.ByteArray import *
from server.helpers.String import *

class StaffChat:
	C, CC = 6, 10

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		chatID = packet.readByte()
		message = String.filtreChatString(packet.readUTF())

		k = ByteArray().writeByte(chatID).writeUTF(users.parsePlayerName(player)).writeUTF(message).writeBoolean(False).writeBoolean(False).writeByte(0)
		for player2 in users.players.values():
			if chatID == 0 and player.privLevel >= 5:
				users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 1 and player.privLevel >= 5:
				users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 2 and player.privLevel >= 3:
				if  player2.privLevel >= 3 and player2.langueID == player.langueID:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 3 and player.privLevel >= 5:
				if player2.privLevel >= 5 and player2.langueID == player.langueID:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 4 and player.privLevel >= 5:
				if player2.privLevel >= 5:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 5 and player.privLevel >= 3:
				if player2.privLevel >= 3:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 7 and player.isMapcrew:
				if player2.isMapcrew and player2.langueID == player.langueID:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 8 and player.isLuacrew:
				if player2.isLuacrew and player2.langueID == player.langueID:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			elif chatID == 9 and player.isFuncorp:
				if player2.isFuncorp and player2.langueID == player.langueID:
					users.sendPacket(player2.channel, [6, 10], k.toByteArray())
			else:
				break