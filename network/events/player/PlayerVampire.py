from network.packet.ByteArray import *

class PlayerVampire:
	C, CC = 8, 66

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		if player.room.isSurvivor:
			player.isVampire = True
			player.room.vampiresList.append(player.playerCode)
			player.room.rooms.sendAll(room, [8, 66], ByteArray().writeInt(player.playerCode).writeInt(-1).toByteArray())

			if room.isQuarentine:
				for player2 in room.players.values():
					users.sendMessage2(player2.channel, "<R><b>{}</b> foi infectado!</R>".format(users.parsePlayerName(player)))