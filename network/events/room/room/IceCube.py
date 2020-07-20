from network.packet.ByteArray import *

class IceCube:
	C, CC = 5, 21

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		playerCode = packet.readInt()
		px = packet.readShort()
		py = packet.readShort()

		if player.isShaman and not player.isDead and room.playersInPlace > 1:
			if player.iceCount != 0 and playerCode != player.playerCode:
				for player2 in room.players.values():
					if player2.playerCode == playerCode and not player2.isShaman:
						player2.isDead = True
						player2.playerScore += 1
						users.sendPlayerDied(player2)
						users.sendPlaceObject(player2, room, room.lastObjectID + 2, 54, px, py, 0, 0, 0, True, True)
						player.iceCount -= 1