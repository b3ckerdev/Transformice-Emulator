import time
from server.helpers.Timer import *

class Conjuration:
	C, CC = 4, 14

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room

		room.rooms.sendAllOthersOld(player, room, [4, 14], values)

		def d(room, roundsRunned):
			time.sleep(10)
			if roundsRunned != room.roundsRunned:
				return
			room.rooms.sendAllOld(room, [4, 15], values)
		Timer.executor.submit(d, (room, room.roundsRunned))