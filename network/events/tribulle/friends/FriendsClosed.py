from network.packet.ByteArray import *

class FriendsClosed:
	code = 30

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()

		player = channel.player
		
		player.friendsOpen = False

		users.server.tribulle.sendTribullePacket(channel.player, 31, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())