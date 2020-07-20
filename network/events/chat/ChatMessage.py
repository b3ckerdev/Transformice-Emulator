import json
from server.helpers.String import *

class ChatMessage:
	C, CC = 6, 6

	@staticmethod
	def parse(users, channel, packet, packetID):
		message = users.chatMessageFilter(String.filtreChatString(packet.readUTF()))
		player = channel.player

		t = int(users.server.getTime() - player.lastChatMessageTime)
		accountTime = player.playingTime + int(users.server.getTime() - player.connectedTime)

		if len(message) == 0:
			return

		elif len(message) > 80 and accountTime < 72000:
			return

		elif len(message) > 200:
			return

		elif users.parsePlayerName(player) in users.server.mutes:
			mute = users.server.mutes[users.parsePlayerName(player)]
			h = users.server.getHoursDiff(mute["time"])
			if h > 0:
				users.sendLangueMessage(channel, player.langue.lower(), "<ROSE>$MuteInfo1", [str(h), mute["reason"]])
				return
			else:
				del users.server.mutes[users.parsePlayerName(player)]
				json.dump(users.server.mutes, open("./json/mutes.json", "w"))

		elif player.lastChatMessage == message:
			users.sendLangueMessage(channel, player.langue.lower(), "$Message_Identique", [])

		elif t < 1:
			users.sendLangueMessage(channel, player.langue.lower(), "$Doucement", [])

		else:
			users.sendChatMessage(channel, player.playerCode, users.parsePlayerName(player), player.langueID, message, False)
			player.chatLog["room"].append(message)

			if users.filterDisclosure(message):
				users.sendMessageToPriv(5, "{} sent a suspicious message in room {} (/chatlog {}).".format(users.parsePlayerName(player), player.room.roomName, users.parsePlayerName(player)), False)