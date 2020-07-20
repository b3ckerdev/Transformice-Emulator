from network.packet.ByteArray import *

class TribeOpen:
	code = 108

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		isOpen = packet.readBoolean()

		player = channel.player
		player.tribeOpen = isOpen