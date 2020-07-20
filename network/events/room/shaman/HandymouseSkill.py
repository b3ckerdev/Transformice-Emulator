from network.packet.ByteArray import *

class HandymouseSkill:
	C, CC = 5, 35

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		handyMouseByte = packet.readByte()
		objectID = packet.readInt()

		if room.lastHandymouse[0] == -1:
			room.lastHandymouse = [objectID, handyMouseByte]
		else:
			users.server.rooms.sendAll(room, [5, 35], ByteArray().writeByte(handyMouseByte).writeInt(objectID).writeByte(room.lastHandymouse[1]).writeInt(room.lastHandymouse[0]).toByteArray())
			users.server.rooms.sendAll(room, [5, 40], ByteArray().writeByte(77).writeByte(1).toByteArray())
			room.lastHandymouse = [-1, -1]