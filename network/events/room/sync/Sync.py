from network.packet.ByteArray import *

class Sync:
	C, CC = 4, 3

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		roundCode = packet.readInt()
		if roundCode == room.lastCodePartie and room.rooms.getPlayersCount(room) >= 2:
			packet2 = ByteArray()
			while packet.bytesAvailable():
				packet2.writeShort(packet.readShort())
				code = packet.readShort()
				packet2.writeShort(code).writeBytes(packet.readBytes(14) if code != -1 else b"")
				if code != -1:
					packet2.writeBoolean(True)
                    
				if ((((room.roundTime + room.addTime) * 1000) + (room.gameStartTimeMillis - int(users.server.getTime()))) > 5000):
					room.rooms.sendAllOthers(player, room, [4, 3], packet2.toByteArray())