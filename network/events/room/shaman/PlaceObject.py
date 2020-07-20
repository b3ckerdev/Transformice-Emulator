from network.packet.ByteArray import *

class PlaceObject:
	C, CC = 5, 20

	@staticmethod
	def parse(users, channel, packet, packetID):
		codePartie = packet.readByte()
		objectID = packet.readInt()
		code = packet.readShort()
		posX = packet.readShort()
		posY = packet.readShort()
		angle = packet.readShort()
		velX = packet.readByte()
		velY = packet.readByte()
		dur = packet.readByte()
		origin = packet.readByte()
		i = packet.readUnsignedInt()

		player = channel.player
		room = player.room
		if codePartie == room.lastCodePartie:
			users.sendPlaceObject(player, room, objectID, code, posX, posY, angle, velX, velY, dur, False)
			users.skills.placeSkill(player, room, objectID, code, posX, posY, angle)