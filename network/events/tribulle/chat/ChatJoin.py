import re
from network.packet.ByteArray import *

class ChatJoin:
	code = 54

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		chatName = packet.readUTF()

		player = channel.player

		if not re.match("^[ a-zA-Z0-9]*$", chatName):
			users.server.tribulle.sendTribullePacket(channel.player, 55, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())
		elif chatName == "V.I.P":
			users.server.tribulle.sendTribullePacket(channel.player, 55, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())
		else:
			if not chatName in users.server.chats:
				users.server.chats[chatName] = []

			if len(users.server.chats[chatName]) >= 200:
				users.server.tribulle.sendTribullePacket(channel.player, 55, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
			else:
				users.server.chats[chatName].append(users.parsePlayerName(player))

				player.chats.append(chatName)

				users.server.tribulle.sendChatJoin(player, chatName)
				users.server.tribulle.sendTribullePacket(player, 55, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())