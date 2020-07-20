from network.packet.ByteArray import *

class IgnoredsList:
	code = 46

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()

		player = channel.player

		users.server.tribulle.sendIgnoredsList(player, tribulleID)