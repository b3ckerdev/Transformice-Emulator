import json
from server.helpers.String import *
from network.packet.ByteArray import *

class ChatWhisper:
	code = 52

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()
		message = users.chatMessageFilter(String.filtreChatString(packet.readUTF()))

		player = channel.player

		t = int(users.server.getTime() - player.lastChatMessageTime)
		accountTime = player.playingTime + int(users.server.getTime() - player.connectedTime)

		if not playerName in users.players:
			users.server.tribulle.sendTribullePacket(channel.player, 53, ByteArray().writeInt(tribulleID).writeByte(12).writeUTF("").toByteArray())
			return

		if playerName in player.ignoredsList:
			users.server.tribulle.sendTribullePacket(channel.player, 53, ByteArray().writeInt(tribulleID).writeByte(27).writeUTF("").toByteArray())
			return

		if users.parsePlayerName(player) in users.server.mutes:
			mute = users.server.mutes[users.parsePlayerName(player)]
			h = users.server.getHoursDiff(mute["time"])
			if h > 0:
				users.server.tribulle.sendTribullePacket(channel.player, 53, ByteArray().writeInt(tribulleID).writeByte(23).toByteArray())
				return
			else:
				del users.server.mutes[users.parsePlayerName(player)]
				json.dump(users.server.mutes, open("./json/mutes.json", "w"))

		if player.whisperCount >= 5:
			if users.server.getTime() - player.whisperTime >= 60:
				player.whisperCount = 0
			else:
				users.server.tribulle.sendTribullePacket(player, 53, ByteArray().writeInt(tribulleID).writeByte(24).writeUTF("").toByteArray())
				return

		if len(message) > 80 and accountTime < 72000:
			users.server.tribulle.sendTribullePacket(player, 53, ByteArray().writeInt(tribulleID).writeByte(22).writeUTF("").toByteArray())
			return

		if len(message) > 200:
			users.server.tribulle.sendTribullePacket(player, 53, ByteArray().writeInt(tribulleID).writeByte(22).writeUTF("").toByteArray())
			return

		player2 = users.players[playerName]

		if player2.silenceType == 2 and not users.parsePlayerName(player) in player2.friendsList:
			users.server.tribulle.sendTribullePacket(player, 53, ByteArray().writeInt(tribulleID).writeByte(25).writeUTF(player2.silenceMessage).toByteArray())
			return

		if users.server.getTime() - player.whisperTime < 3:
			player.whisperCount += 1
		else:
			player.whisperCount = 0

		if player != player2:
			users.server.tribulle.sendTribullePacket(player2, 66, ByteArray().writeUTF(users.parsePlayerName(player).lower()).writeInt(player.langueID + 1).writeUTF(playerName.lower()).writeUTF(message).toByteArray())

		users.server.tribulle.sendTribullePacket(player, 66, ByteArray().writeUTF(users.parsePlayerName(player).lower()).writeInt(player.langueID + 1).writeUTF(playerName.lower()).writeUTF(message).toByteArray())
		users.server.tribulle.sendTribullePacket(channel.player, 53, ByteArray().writeInt(tribulleID).writeByte(1).writeUTF("").toByteArray())

		player.whisperTime = users.server.getTime()

		if not playerName in list(player.chatLog["whisper"]):
			player.chatLog["whisper"][playerName] = []

		player.chatLog["whisper"][playerName].append(message)

		if users.filterDisclosure(message):
			users.sendMessageToPriv(5, "{} sent a suspicious message to {} (/chatlog {}).".format(users.parsePlayerName(player), playerName, users.parsePlayerName(player)), False)