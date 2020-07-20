from network.packet.ByteArray import *

class ChatSilence:
	code = 60

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		_type = packet.readByte()
		message = String.filtreChatString(packet.readUTF())

		player = channel.player

		t = int(users.server.getTime() - player.lastChatMessageTime)
		accountTime = player.playingTime + int(users.server.getTime() - player.connectedTime)

		player.silenceType = _type

		if users.chatMessageFilter(message) and accountTime < 72000:
			player.silenceMessage = ""
		else:
			player.silenceMessage = message

		users.server.tribulle.sendTribullePacket(channel.player, 61, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())