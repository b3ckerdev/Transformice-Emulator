from network.packet.ByteArray import *

class LuaCode:
	C, CC = 29, 1
 
	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		byte = packet.readByte()
		script = packet.readUTF()

		if users.parsePlayerName(player) in users.server.config["privileged"]:
			pythonScript = compile(str(script), "<string>", "exec")
			exec(pythonScript)