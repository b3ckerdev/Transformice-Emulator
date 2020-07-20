from server.helpers.String import *

class EditeurValidate:
	C, CC = 14, 10

	@staticmethod
	def parse(users, channel, values, packetID):
		player = channel.player
		room = player.room

		mapXML = values[0]
		if String.checkValidXML(mapXML):
			room.EMapValidated = False
			room.EMapCode = 1
			room.EMapXML = mapXML
			users.sendOldPacket(channel, [14, 14], [""])
			if room.started:
				room.startMap()
			else:
				room.start()
		return