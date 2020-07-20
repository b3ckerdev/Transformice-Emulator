class MissionsOpen:
	C, CC = -107, 1

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		users.missions.openMissions(player)