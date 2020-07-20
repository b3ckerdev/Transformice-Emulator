from network.packet.ByteArray import *

class Missions:
	def __init__(self, users):
		self.users = users
		self.server = users.server

	def openMissions(self, player):
		packet = ByteArray()
		packet.writeUnsignedByte(len(list(player.missions)))
		for id, values in player.missions.items():
			packet.writeUnsignedShort(id)
			packet.writeUnsignedByte(values[0])
			packet.writeUnsignedShort(values[1])
			packet.writeUnsignedShort(values[2])
			packet.writeUnsignedShort(values[3])
			packet.writeUnsignedShort(0)
			packet.writeBoolean(False)
		self.users.sendPacket(player.channel, [144, 3], packet.toByteArray())
