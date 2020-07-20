import random
from network.packet.ByteArray import *

class CorrectVersion:
	C, CC = 28, 1

	@staticmethod
	def parse(users, channel, packet, packetID):
		version = packet.readShort()
		connectionKey = packet.readUTF()
		standType = packet.readUTF()
		traceI = packet.readUTF()
		intTyp = packet.readInt()
		strV = packet.readUTF()
		stringCode = packet.readUTF()
		windowInfo = packet.readUTF()
		integerT = packet.readInt()
		integerY = packet.readInt()
		strL = packet.readUTF()
		print(version, connectionKey)

		if version != users.server.config["protection"]["version"]:
			channel.close_connection()
		elif connectionKey != users.server.config["protection"]["key"]:
			channel.close_connection()
		else:
			channel.player.loginXor = random.randint(0, 500000)
			channel.isValidated = True

			l = "en"
			if channel.geoIP.match():
				l = users.server.langues.getLangue(users.server.langues.getLangueByName(channel.geoIP.json["country_code"].lower()))

			if standType != "PlugIn":
				channel.player.isStandAlone = True
				
			users.sendPacket(channel, [26, 3], ByteArray().writeInt(len(users.players)).writeByte(packetID).writeUTF(l.lower()).writeUTF(l.lower()).writeInt(channel.player.loginXor).writeBoolean(False).toByteArray())