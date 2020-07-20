from network.packet.ByteArray import *

class Map26:
	C, CC = 5, 8

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		if room.currentMap == 26:
			posX = packet.readShort()
			posY = packet.readShort()
			width = packet.readShort()
			height = packet.readShort()

			bodyDef = {}
			bodyDef["width"] = width
			bodyDef["height"] = height
			room.rooms.sendAll(room, [29, 28], ByteArray().writeShort(0).writeBoolean(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef else 0).writeShort(posX).writeShort(posY).writeShort(int(bodyDef["width"]) if "width" in bodyDef else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef else 0).writeBoolean(bool(bodyDef["foreground"]) if "foreground" in bodyDef else False).writeShort(int(bodyDef["friction"]) if "friction" in bodyDef else 0).writeShort(int(bodyDef["restitution"]) if "restitution" in bodyDef else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef else 0).writeBoolean("color" in bodyDef).writeInt(int(bodyDef["color"]) if "color" in bodyDef else 0).writeBoolean(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef else True).writeBoolean(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef else True).writeBoolean(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef else 0).writeShort(int(bodyDef["linearDamping"]) if "linearDamping" in bodyDef else 0).writeShort(int(bodyDef["angularDamping"]) if "angularDamping" in bodyDef else 0).writeBoolean(False).writeUTF("").toByteArray())