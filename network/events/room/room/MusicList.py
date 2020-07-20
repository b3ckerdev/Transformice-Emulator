from network.packet.ByteArray import *

class MusicList:
	C, CC = 5, 73

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		if room.isMusic:
			p = ByteArray().writeShort(len(room.musicList))
			for playerName, data in room.musicList.items():
				p.writeUTF(playerName)
				p.writeUTF(data["items"][0]["snippet"]["title"])
			users.sendPacket(channel, [5, 73], p.toByteArray())