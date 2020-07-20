from server.helpers.String import *
from server.helpers.YoutubeAPI import *

class MusicSend:
	C, CC = 5, 70

	@staticmethod
	def parse(users, channel, packet, packetID):
		key = String.getYoutubeID(packet.readUTF())

		player = channel.player
		room = player.room

		if room.isMusic and key != None:
			if users.parsePlayerName(player) in room.musicList:
				users.sendLangueMessage(channel, player.langue.lower(), "$ModeMusic_VideoEnAttente", [])
			else:
				youtube = YoutubeAPI(users, channel, room, key)