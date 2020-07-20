from network.packet.ByteArray import *

class ChatLeave:
	code = 56

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		chatName = packet.readUTF()

		player = channel.player

		if chatName in users.server.chats:
			n = users.parsePlayerName(player)
			if n in users.server.chats[chatName]:
				users.server.chats[chatName].remove(n)

				if len(users.server.chats[chatName]) == 0:
					del users.server.chats[chatName]

			if chatName in player.chats:
				player.chats.remove(chatName)

		users.server.tribulle.sendTribullePacket(player, 63, ByteArray().writeUTF(chatName).toByteArray())