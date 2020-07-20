from server.helpers.String import *
from network.packet.ByteArray import *

class TChatMessage:
	code = 48

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		chatName = packet.readUTF()
		message = users.chatMessageFilter(String.filtreChatString(packet.readUTF()))

		player = channel.player

		if len(message) > 80 and accountTime < 72000:
			return
		elif not chatName in users.server.chats:
			users.server.tribulle.sendTribullePacket(player, 49, ByteArray().writeInt(tribulleID).writeByte(0).toByteArray())
		else:
			for playerName in users.server.chats[chatName]:
				if playerName in users.players:
					player2 = users.players[playerName]
					users.server.tribulle.sendTribullePacket(player2, 64, ByteArray().writeUTF(users.parsePlayerName(player).lower()).writeInt(player.langueID + 1).writeUTF(chatName).writeUTF(message).toByteArray())

			users.server.tribulle.sendTribullePacket(player, 49, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
			player.chatLog["room"].append(message)

			if users.filterDisclosure(message):
				users.sendMessageToPriv(5, "{} sent a suspicious message in chat {} (/chatlog {}).".format(users.parsePlayerName(player), chatName, users.parsePlayerName(player)), False)