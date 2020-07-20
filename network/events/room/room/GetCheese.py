from network.packet.ByteArray import *

class GetCheese:
	C, CC = 5, 19

	@staticmethod
	def parse(users, channel, packet, packetID):
		codePartie = packet.readInt()
		cheeseX = packet.readShort()
		cheeseY = packet.readShort()
		distance = packet.readShort()

		player = channel.player
		room = player.room

		if codePartie == player.room.lastCodePartie:
			player.hasCheese = True
			
			if room.isTutorial:
				users.sendPacket(channel, [5, 90], ByteArray().writeByte(1).toByteArray())

			users.server.rooms.sendAll(room, [144, 6], ByteArray().writeInt(player.playerCode).writeBoolean(True).toByteArray())