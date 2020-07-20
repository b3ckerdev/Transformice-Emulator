from network.packet.ByteArray import *

class EnterRoom:
	C, CC = 5, 38

	@staticmethod
	def parse(users, channel, packet, packetID):
		isInternational = packet.readBoolean()
		roomName = packet.readUTF()

		if roomName == "":
			users.enterRoom(channel.player, users.server.rooms.getRecommendRoom(users.server.langues.getLangue(channel.player.langueID)))
		else:
			if roomName[:1] == "*":
				if roomName in users.server.rooms.rooms:
					room = users.server.rooms.rooms[roomName]
					if room.roomPassword != "":
						users.sendPacket(channel, [5, 39], ByteArray().writeUTF(roomName).toByteArray())
						return
						
			users.enterRoom(channel.player, roomName)