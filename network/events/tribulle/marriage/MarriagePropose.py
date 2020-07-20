from server.helpers.Timer import *
from network.packet.ByteArray import *

class MarriagePropose:
	code = 22

	@staticmethod
	def parse(users, channel, packet, packetID):
		tribulleID = packet.readInt()
		playerName = packet.readUTF().capitalize()

		player = channel.player

		if not playerName in users.players:
			users.server.tribulle.sendTribullePacket(player, 23, ByteArray().writeInt(tribulleID).writeByte(11).toByteArray())
		elif users.players[playerName].marriage != "":
			users.server.tribulle.sendTribullePacket(player, 23, ByteArray().writeInt(tribulleID).writeByte(15).toByteArray())
		elif player.marriageInvite != "":
			users.server.tribulle.sendTribullePacket(player, 23, ByteArray().writeInt(tribulleID).writeByte(6).toByteArray())
		elif playerName in player.ignoredsList:
			users.server.tribulle.sendTribullePacket(player, 23, ByteArray().writeInt(tribulleID).writeByte(4).toByteArray())
		else:
			player.marriageInvite = playerName
			
			def d(pl):
				if not pl.channel.isClosed:
					pl.marriageInvite = ""
			t = Timer.executor.submit(d, (channel.player))

			player2 = users.players[playerName]
			users.server.tribulle.sendTribullePacket(player2, 38, ByteArray().writeUTF(users.parsePlayerName(player).lower()).toByteArray())
			
			users.server.tribulle.sendTribullePacket(player, 23, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
