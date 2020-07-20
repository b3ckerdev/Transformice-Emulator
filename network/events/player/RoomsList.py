from network.packet.ByteArray import *

class RoomsList:
	C, CC = 26, 35

	@staticmethod
	def parse(users, channel, packet, packetID):
		mode = packet.readByte()

		if mode == 0:
			mode = 1

		channel.player.roomsListMode = mode

		packet2 = ByteArray()
		packet2.writeByte(len(users.server.rooms.roomsType))
		for _type in users.server.rooms.roomsType:
			packet2.writeByte(_type)

		packet2.writeByte(mode)

		name = {9: "racing", 1: "", 10: "defilante", 2: "bootcamp", 8: "survivor", 3: "vanilla", 11: "music", 16: "village", 18: "minigame"}[mode]
		packet2.writeByte(1)
		packet2.writeUnsignedByte(channel.player.langueID)
		packet2.writeUTF("{} {}".format(users.server.config["name"], name))
		packet2.writeUTF(str(users.server.rooms.getPlayersCountForMode(mode)))
		packet2.writeUTF("mjj")
		packet2.writeUTF("1")

		for roomName, room in users.server.rooms.rooms.items():
			if room.roomType == mode:
				if not room.roomName[:1].lower() in ["*", "\x03"] or room.isPublic:
					if room.roomName[:2].lower() == channel.player.langue.lower() or room.isPublic:
						packet2.writeByte(0)
						packet2.writeUnsignedByte(users.server.langues.getLangueByName(room.roomName[:2]))
						packet2.writeUTF(roomName if room.isPublic else roomName[3:])
						packet2.writeUnsignedShort(users.server.rooms.getPlayersCount(room))
						packet2.writeUnsignedByte(0 if not room.isLimitedPlayers else room.maxPlayers)
						packet2.writeBoolean(room.isFuncorp)

		if mode == 8:
			if not "{}-quarentine1".format(channel.player.langue.lower()) in users.server.rooms.rooms:
				packet2.writeByte(0)
				packet2.writeUnsignedByte(users.server.langues.getLangueByName(channel.player.langue.lower()))
				packet2.writeUTF("quarentine1")
				packet2.writeUnsignedShort(0)
				packet2.writeUnsignedByte(0)
				packet2.writeBoolean(False)

		if mode == 9:
			if not "{}-fastracing1".format(channel.player.langue.lower()) in users.server.rooms.rooms:
				packet2.writeByte(0)
				packet2.writeUnsignedByte(users.server.langues.getLangueByName(channel.player.langue.lower()))
				packet2.writeUTF("fastracing1")
				packet2.writeUnsignedShort(0)
				packet2.writeUnsignedByte(0)
				packet2.writeBoolean(False)

		users.sendPacket(channel, [26, 35], packet2.toByteArray())