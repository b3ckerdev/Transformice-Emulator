from network.packet.ByteArray import *

class RedistributeSkills:
	C, CC = 8, 22

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		price = 0
		for count in player.playerSkills.values():
			price += count

		if player.playerID in users.server.cache.redistributeSkillsTime:
			if users.server.getTime() - users.server.cache.redistributeSkillsTime[player.playerID] < 600:
				users.sendPacket(channel, [24, 3], b"")
				return
			else:
				del users.server.cache.redistributeSkillsTime[player.playerID]

		if player.shopCheeses < price:
			users.sendPacket(channel, [24, 4], b"")
		else:
			player.playerSkills = {}
			player.shopCheeses -= price
			users.server.cache.redistributeSkillsTime[player.playerID] = users.server.getTime()
			users.skills.sendShamanSkills(channel, True)