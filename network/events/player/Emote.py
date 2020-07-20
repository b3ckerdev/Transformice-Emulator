import random
from network.packet.ByteArray import *

class Emote:
	C, CC = 8, 1

	@staticmethod
	def parse(users, channel, packet, packetID):
		emoteID = packet.readByte()
		playerCode = packet.readInt()
		flag = packet.readUTF() if packet.bytesAvailable() else ""

		player = channel.player
		room = channel.player.room

		users.sendPlayerEmote(player, room, emoteID, flag, True, False)

		if playerCode != -1:
			if emoteID == 14:
				users.sendPlayerEmote(player, room, 14, flag, False, False)
				users.sendPlayerEmote(player, room, 15, flag, False, False)
				player2 = None
				for p in room.players.values():
					if p.playerCode == playerCode:
						player2 = p
				if player2 != None:
					users.sendPlayerEmote(player2, room, 14, flag, False, False)
					users.sendPlayerEmote(player2, room, 15, flag, False, False)

			elif emoteID == 18:
				users.sendPlayerEmote(player, room, 18, flag, False, False)
				users.sendPlayerEmote(player, room, 19, flag, False, False)
				player2 = None
				for p in room.players.values():
					if p.playerCode == playerCode:
						player2 = p
				if player2 != None:
					users.sendPlayerEmote(player2, room, 17, flag, False, False)
					users.sendPlayerEmote(player2, room, 19, flag, False, False)

			elif emoteID == 22:
				users.sendPlayerEmote(player, room, 22, flag, False, False)
				users.sendPlayerEmote(player, room, 23, flag, False, False)
				player2 = None
				for p in room.players.values():
					if p.playerCode == playerCode:
						player2 = p
				if player2 != None:
					users.sendPlayerEmote(player2, room, 22, flag, False, False)
					users.sendPlayerEmote(player2, room, 23, flag, False, False)

			elif emoteID == 26:
				users.sendPlayerEmote(player, room, 26, flag, False, False)
				users.sendPlayerEmote(player, room, 27, flag, False, False)
				player2 = None
				for p in room.players.values():
					if p.playerCode == playerCode:
						player2 = p
				if player2 != None:
					users.sendPlayerEmote(player2, room, 26, flag, False, False)
					users.sendPlayerEmote(player2, room, 27, flag, False, False)
					room.rooms.sendAll(room, [100, 5], ByteArray().writeInt(player.playerCode).writeByte(random.choice([0, 1, 2])).writeInt(player2.playerCode).writeByte(random.choice([0, 1, 2])).toByteArray())

		if player.isShaman:
			users.skills.parseEmoteSkill(player, room, emoteID)