from network.packet.ByteArray import *

class FriendsList:
	code = 28

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()

		player = channel.player
		
		player.friendsOpen = True

		users.server.tribulle.sendFriendsList(channel.player)
		users.server.tribulle.sendTribullePacket(channel.player, 29, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())