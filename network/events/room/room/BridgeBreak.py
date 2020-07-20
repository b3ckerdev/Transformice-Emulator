from network.packet.ByteArray import *

class BridgeBreak:
	C, CC = 5, 24

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player
		room = player.room

		bridgeCode = packet.readShort()
		room.rooms.sendAllOthers(player, room, [5, 24], ByteArray().writeShort(bridgeCode).toByteArray())