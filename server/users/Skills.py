import threading
from network.packet.ByteArray import *

class Skills:
	def __init__(self, users, rooms):
		self.users = users
		self.rooms = rooms

	def sendExp(self, channel, level, exp, nextLevel):
		self.users.sendPacket(channel, [8, 8], ByteArray().writeShort(level - 1).writeInt(exp).writeInt(nextLevel).toByteArray())

	def sendGainExp(self, channel, amount):
		self.users.sendPacket(channel, [8, 9], ByteArray().writeInt(amount).toByteArray())

	def sendEarnedExp(self, channel, xp, numCompleted):
		self.users.sendPacket(channel, [24, 1], ByteArray().writeShort(xp).writeShort(numCompleted).toByteArray())

	def sendEarnedLevel(self, channel, playerName, level):
		self.rooms.sendAll(channel.player.room, [24, 2], ByteArray().writeUTF(playerName).writeShort(level - 1).toByteArray())

	def sendEnableSkill(self, channel, id, count):
		self.users.sendPacket(channel, [8, 10], ByteArray().writeUnsignedByte(id).writeUnsignedByte(count).toByteArray())

	def sendShamanFly(self, player, fly):
		self.rooms.sendAllOthers(player, player.room, [8, 15], ByteArray().writeInt(player.playerCode).writeBoolean(fly).toByteArray())

	def sendShamanSkills(self, channel, refresh):
		packet = ByteArray().writeByte(len(channel.player.playerSkills))
		for skillID, count in channel.player.playerSkills.items():
			packet.writeByte(skillID)
			packet.writeByte(count)
		self.users.sendPacket(channel, [8, 22], packet.writeBoolean(refresh).toByteArray())

	def earnExp(self, player, exp, saveds=0):
		player.shamanExp += exp

		if player.shamanExp > player.shamanExpNext:
			player.shamanLevel += 1
			player.shamanExp -= player.shamanExpNext
			player.shamanExpNext += 90

			self.sendExp(player.channel, player.shamanLevel, player.shamanExp, player.shamanExpNext)
			self.sendGainExp(player.channel, player.shamanExp)

			if player.isShaman:
				self.sendEarnedExp(player.channel, exp, saveds)

			self.sendEarnedLevel(player.channel, self.users.parsePlayerName(player), player.shamanLevel)
		else:
			if exp > 0:
				self.sendGainExp(player.channel, player.shamanExp)
				self.sendExp(player.channel, player.shamanLevel, player.shamanExp, player.shamanExpNext)

			if player.isShaman:
				self.sendEarnedExp(player.channel, exp, saveds)

	def buySkill(self, player, id):
		if not id in player.playerSkills:
			player.playerSkills[id] = 0
		player.playerSkills[id] += 1
		self.sendShamanSkills(player.channel, True)

	def checkQualifiedPlayer(self, player, px, py, player2):
		if not player2 != player and not player2.isShaman:
			if player2.posX >= px - 85 and player2.posX <= px + 85:
				if player2.posY >= py - 85 and player2.posY <= py + 85:
					return True
		return False

	def getPlayerSkills(self, player, skills):
		if 1 in skills:
			count = skills[1]
			self.sendEnableSkill(player.channel, 1, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

		if 2 in skills:
			count = skills[2]
			self.sendEnableSkill(player.channel, 2, [114, 126, 118, 120, 122][(5 if count > 5 else count) - 1])

		if 68 in skills:
			count = skills[68]
			self.sendEnableSkill(player.channel, 68, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])

	def getShamanSkills(self, player):
		if 4 in player.playerSkills and not player.room.isDoubleShaman:
			player.canShamanRespawn = True

		for skill in [5, 8, 9, 11, 12, 26, 28, 29, 31, 41, 46, 48, 51, 52, 53, 60, 62, 65, 66, 67, 69, 71, 74, 80, 81, 83, 85, 88, 90, 93]:
			if skill == 5 and player.room.isSurvivor:
				continue

			if skill in player.playerSkills and not (player.room.isSurvivor and skill == 81):
				self.sendEnableSkill(player.channel, skill, player.playerSkills[skill] * 2 if skill == 28 or skill == 65 or skill == 74 else player.playerSkills[skill])

		for skill in [6, 10, 13, 30, 33, 34, 44, 47, 50, 63, 64, 70, 73, 82, 84, 92]:
			if skill == 82 and player.room.isSurvivor:
				continue

			if skill in player.playerSkills:
				self.sendEnableSkill(player.channel, skill, 3 if skill == 10 or skill == 13 else 1)

		for skill in [7, 14, 27, 54, 86, 87, 94]:
			if skill == 27 and player.room.isSurvivor:
				continue
				
			if skill in player.playerSkills:
				self.sendEnableSkill(player.channel, skill, 130 if skill == 54 else 100)

		if 20 in player.playerSkills:
			count = player.playerSkills[20]            
			self.sendEnableSkill(player.channel, 20, [114, 126, 118, 120, 122][(5 if count > 5 else count) - 1])

		if 21 in player.playerSkills:
			player.room.bubblesCount += player.playerSkills[21]

		if 22 in player.playerSkills:
			count = player.playerSkills[22]
			self.sendEnableSkill(player.channel, 22, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

		if 23 in player.playerSkills:
			count = player.playerSkills[23]            
			self.sendEnableSkill(player.channel, 23, [40, 50, 60, 70, 80][(5 if count > 5 else count) - 1])

		if 24 in player.playerSkills:
			player.isOpportunist = True

		if 32 in player.playerSkills:
			player.iceCount += player.playerSkills[32]

		if 40 in player.playerSkills:
			count = player.playerSkills[40]            
			self.sendEnableSkill(player.channel, 40, [30, 40, 50, 60, 70][(5 if count > 5 else count) - 1])

		if 42 in player.playerSkills:
			count = player.playerSkills[42]            
			self.sendEnableSkill(player.channel, 42, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

		if 43 in player.playerSkills:
			count = player.playerSkills[43]            
			self.sendEnableSkill(player.channel, 43, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

		if 45 in player.playerSkills:
			count = player.playerSkills[45]            
			self.sendEnableSkill(player.channel, 45, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

		if 49 in player.playerSkills:
			count = player.playerSkills[49]
			self.sendEnableSkill(player.channel, 49, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

		if 72 in player.playerSkills:
			count = player.playerSkills[72]            
			self.sendEnableSkill(player.channel, 72, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

		if 89 in player.playerSkills:
			if skill == 27 and player.room.isSurvivor:
				return
			count = player.playerSkills[89]            
			self.sendEnableSkill(player.channel, 49, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])
			self.sendEnableSkill(player.channel, 54, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])

		if 91 in player.playerSkills:
			player.desintegration = True

	def sendTeleport(self, player, _type, posX, posY):
		self.rooms.sendAll(player.room, [5, 50], ByteArray().writeByte(_type).writeShort(posX).writeShort(posY).toByteArray())

	def movePlayer(self, player, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
		self.users.sendPacket(player.channel, [8, 3], ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

	def sendSkillObject(self, room, objectID, posX, posY, angle):
		self.rooms.sendAll(room, [5, 14], ByteArray().writeShort(posX).writeShort(posY).writeByte(objectID).writeShort(angle).toByteArray())

	def placeSkill(self, player, room, objectID, code, px, py, angle):
		if code == 36:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					self.users.sendPacket(player2.channel, [27, 10], ByteArray().writeByte(1).toByteArray())
					break

		elif code == 37:
			for player2 in room.players.values():
				if not player2.isDead:
					if self.checkQualifiedPlayer(player, px, py, player2):
						self.sendTeleport(player, 36, player2.posX, player2.posY)
						self.movePlayer(player2, player.posX, player.posY, False, 0, 0, True)
						self.sendTeleport(player, 37, player.posX, player.posY)
						break

		elif code == 38:
			if room.isSurvivor:
				return

			for player2 in room.players.values():
				if player2.isDead and not player2.hasEnter and not player2.isAfk and not player2.isShaman:
					hasCheese = player2.hasCheese
					self.users.respawnSpecific(player2)
					player2.hasCheese = hasCheese
					if room.playersInPlace >= 1 and player2.hasCheese:
						player2.hasCheese = False
						room.rooms.sendAll(room, [144, 6], ByteArray().writeInt(player2.playerCode).writeBoolean(True).toByteArray())
					player.isDead = False
					self.movePlayer(player2, player.posX, player.posY, False, 0, 0, True)
					self.sendTeleport(player2, 37, player2.posX, player2.posY)
					break

		elif code == 42:
			self.sendSkillObject(room, 3, px, py, 0)

		elif code == 43:
			self.sendSkillObject(room, 1, px, py, 0)

		elif code == 47:
			if room.playersInPlace > 0:
				for player2 in room.players.values():
					if not player2.isDead and player2.hasCheese and self.checkQualifiedPlayer(player, px, py, player2):
						self.users.playerWin(player2, 0, room.lastCodePartie, 0, 0, 0, 0)
						break
 
		elif code == 55:
			if player.hasCheese:
				for player2 in room.players.values():
					if not player2.hasCheese and not player2.isDead and self.checkQualifiedPlayer(player, px, py, player2):
						room.rooms.sendAll(room, [144, 6], ByteArray().writeInt(player2.playerCode).writeBoolean(True).toByteArray())
						room.rooms.sendAll(room, [8, 19], ByteArray().writeInt(player.playerCode).toByteArray())
						player2.hasCheese = True
						player.hasCheese = False
						break

		elif code == 56:
			self.sendTeleport(player, 36, player.posX, player.posY)
			self.movePlayer(player, px, py, False, 0, 0, False)
			self.sendTeleport(player, 37, px, py)

		elif code == 57:
			if room.cloudID == -1:
				room.cloudID = objectID
			else:
				room.rooms.sendAll(room, [4, 8], ByteArray().writeInt(room.cloudID).writeBoolean(True).toByteArray())
				room.cloudID = objectID

		elif code == 61:
			if room.companionBox == -1:
				room.companionBox = objectID
			else:
				room.rooms.sendAll(room, [4, 8], ByteArray().writeInt(room.companionBox).writeBoolean(True).toByteArray())
				room.companionBox = objectID

		elif code == 70:
			room.rooms.sendAll(room, [5, 36], ByteArray().writeShort(px).writeShort(py).toByteArray())

		elif code == 71:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					room.rooms.sendAll(room, [5, 30], ByteArray().writeInt(player2.playerCode).toByteArray())
					room.rooms.sendAll(room, [5, 40], ByteArray().writeByte(71).writeByte(1).toByteArray())
					break

		elif code == 73:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					room.rooms.sendAll(room, [5, 31], ByteArray().writeInt(player2.playerCode).writeShort(70).writeBoolean(True).toByteArray())
					break

		elif code == 74:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					room.rooms.sendAll(room, [5, 33], ByteArray().writeByte(1).writeInt(player2.playerCode).toByteArray())
					break

		elif code == 75:
			room.rooms.sendAll(room, [5, 32], b"")

		elif code == 76:
			self.sendSkillObject(room, 5, px, py, angle)

		elif code == 79:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					room.rooms.sendAll(room, [5, 34], ByteArray().writeInt(player2.playerCode).writeBoolean(True).toByteArray())
					t = threading.Timer(player.playerSkills[82] * 2, room.rooms.sendAll, args=[room, [5, 34], ByteArray().writeInt(player2.playerCode).writeBoolean(False).toByteArray()])
					room.reactors.append(t)
					t.start()

		elif code == 81:
			room.rooms.sendAll(room, [5, 28], ByteArray().writeShort(player.playerSkills[63] * 2).writeShort(0).writeShort(0).toByteArray())

		elif code == 83:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					self.users.sendPacket(player2.channel, [8, 39], b"\x01")
					break

		elif code == 84:
			room.rooms.sendAll(room, [5, 37], ByteArray().writeInt(player.playerCode).writeShort(px).writeShort(py).toByteArray())

		elif code == 86:
			room.rooms.sendAll(room, [5, 45], ByteArray().writeShort(px).writeShort(py).writeByte(player.playerSkills[86] * 4).toByteArray())

		elif code == 92:
			room.rooms.sendAll(room, [5, 42], b"")
			self.getShamanSkills(player)

		elif code == 93:
			for player2 in room.players.values():
				if self.checkQualifiedPlayer(player, px, py, player2):
					room.rooms.sendAll(room, [5, 38], ByteArray().writeInt(player2.playerCode).writeUnsignedByte(200).toByteArray())
					break

		elif code == 94:
			room.rooms.sendAll(room, [5, 43], ByteArray().writeInt(player.playerCode).writeByte(1).toByteArray())

	def parseEmoteSkill(self, player, room, emote):
		roomSkills = {}

		if player.playerCode == room.currentShamanCode:
			roomSkills = room.currentShamanSkills
		elif player.playerCode == room.currentShamanCode2:
			roomSkills = room.currentSecondShamanSkills
		else:
			return

		count = 0
		if emote == 0 and 3 in roomSkills:
			for player2 in room.players.values():
				if roomSkills[3] >= count and player2 != player:
					if player2.posX >= player.posX - 400 and player2.posX <= player.posX + 400:
						if player2.posY >= player.posY - 300 and player2.posY <= player.posY + 300:
							self.users.sendPlayerEmote(player2, room, 0, "", False, False)
							count += 1
				else:
					break

		elif emote == 4 and 61 in roomSkills:
			for player2 in room.players.values():
				if roomSkills[61] >= count and player2 != player:
					if player2.posX >= player.posX - 400 and player2.posX <= player.posX + 400:
						if player2.posY >= player.posY - 300 and player2.posY <= player.posY + 300:
							self.users.sendPlayerEmote(player2, room, 2, "", False, False)
							count += 1
				else:
					break

		elif emote == 8 and 25 in roomSkills:
			for player2 in room.players.values():
				if roomSkills[25] >= count and player2 != player:
					if player2.posX >= player.posX - 400 and player2.posX <= player.posX + 400:
						if player2.posY >= player.posY - 300 and player2.posY <= player.posY + 300:
							self.users.sendPlayerEmote(player2, room, 3, "", False, False)
							count += 1
				else:
					break