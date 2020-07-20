import threading
from network.packet.ByteArray import *

class Room(threading.Thread):
	def __init__(self, rooms, roomName):
		threading.Thread.__init__(self)

		self.rooms = rooms
		self.users = rooms.users
		self.roomName = roomName

		self.players = {}

		self.reactors = []
		self.kickeds = []

		self.addTime = 0
		self.roundTime = 0
		self.currentMap = 0
		self.currentXML = ""
		self.currentName = ""
		self.currentPerm = 0
		self.currentInverted = False
		self.roomType = 0
		self.maxPlayers = 25
		self.lastCodePartie = 0
		self.roundsCount = -1
		self.playersInPlace = 0
		self.roundsRunned = 0
		self.gameStartTimeMillis = 0
		self.currentShamanCode = -1
		self.currentShamanName = ""
		self.currentShamanType = 0
		self.currentShamanLevel = 0
		self.currentShamanBadge = 0
		self.currentShamanCode2 = -1
		self.currentShamanName2 = ""
		self.currentShamanType2 = 0
		self.currentShamanLevel2 = 0
		self.currentShamanBadge2 = 0
		self.currentSyncCode = -1
		self.currentSyncName = ""
		self.currentShamanSkills = {}
		self.currentSecondShamanSkills = {}
		self.lastShamanName = ""
		self.lastShamanName2 = ""
		self.holesType = {0: 0, 1: 0, 2: 0, 3: 0}
		self.anchors = []
		self.vampiresList = []
		self.musicList = {}
		self.currentMusicKey = ""
		self.musicStartedTime = 0
		self.bubblesCount = 0
		self.cloudID = -1
		self.companionBox = -1
		self.lastObjectID = 0
		self.showPWinner = False
		self.roomPassword = ""
		self.nextMapID = 0

		self.vampireSelected = False
		self.vampiresRand = []
		self.lastHandymouse = [-1, -1]

		self.isNormRoom = False
		self.isTutorial = False
		self.isEditeur = False
		self.isRacing = False
		self.isFastracing = False
		self.isVanilla = False
		self.isSurvivor = False
		self.isDefilante = False
		self.isBootcamp = False
		self.isMusic = False
		self.isVillage = False
		self.noShaman = False
		self.isFuncorp = False
		self.isPublic = False
		self.isCurrentlyPlay = False
		self.isDoubleShaman = False
		self.catchTheCheeseMap = False
		self.isLimitedPlayers = False
		self.autoRespawn = False
		self.countStats = True
		self.killAllAfk = True
		self.isNoShamanMap = False
		self.noShamanSkills = False
		self.noRemoveRoom = False
		self.isQuarentine = False
		self.isMinigame = False
		self.noRecords = True
		self.EMapValidated = False
		self.EMapCode = 0
		self.EMapXML = ""
		self.count3Seconds = True
		self.leveTest = False
		self.started = False
		self.musicTimer = None
		self.changeTimer = None
		self.killAfkTimer = None
		self.vampireTimer = None

		if "racing" in self.roomName.lower() or "fastracing" in self.roomName.lower():
			self.isRacing = True
			self.roundTime = 60
			self.noShaman = True
			self.roomType = 9
			self.noRecords = False
			if "fastracing" in self.roomName.lower():
				self.isFastracing = True
		elif "\x03[tutorial]" in self.roomName.lower():
			self.isTutorial = True
			self.roundTime = 120
			self.noShaman = True
			self.roomType = 1
			self.countStats = False
		elif "\x03[editeur]" in self.roomName.lower():
			self.isEditeur = True
			self.roundTime = 120
			self.noShaman = True
			self.roomType = 1
			self.countStats = False
			self.killAllAfk = False
		elif "defilante" in self.roomName.lower():
			self.isDefilante = True
			self.roundTime = 60
			self.noShaman = True
			self.roomType = 10
			self.noRecords = False
		elif "bootcamp" in self.roomName.lower():
			self.isBootcamp = True
			self.roundTime = 360
			self.noShaman = True
			self.roomType = 2
			self.autoRespawn = True
		elif "survivor" in self.roomName.lower():
			self.isSurvivor = True
			self.roundTime = 90
			self.roomType = 8
		elif "quarentine" in self.roomName.lower():
			self.isSurvivor = True
			self.isQuarentine = True
			self.roundTime = 60
			self.roomType = 8
			self.noShamanSkills = True
			self.killAllAfk = False
		elif "vanilla" in self.roomName.lower():
			self.isVanilla = True
			self.roundTime = 120
			self.roomType = 3
		elif "music" in self.roomName.lower():
			self.isMusic = True
			self.roundTime = 120
			self.roomType = 11
		#elif "village" in self.roomName.lower():
		#	self.isVillage = True
		#	self.roundTime = 18800
		#	self.roomType = 16
		#	self.countStats = False
		#	self.killAllAfk = False
		#	self.autoRespawn = True
		else:
			self.isNormRoom = True
			self.roundTime = 120
			self.roomType = 1

	def run(self):
		self.started = True
		self.startMap()

	def addClient(self, player):
		player.funColor = ""
		player.funMouseColor = ""
		player.isNewPlayer = True
		
		self.players[self.users.parsePlayerName(player)] = player

		if len(self.players) == 1:
			if not self.isEditeur:
				if self.started:
					self.startMap()
				else:
					self.start()
		else:
			self.users.resetPlayer(player)
			
			player.isDead = True
			
			if not player.isHide:
				self.rooms.sendAllOthers(player, self, [144, 2], ByteArray().writeBytes(self.rooms.server.users.getPlayerData(player)).writeBoolean(False).writeBoolean(True).toByteArray())

			self.users.startPlayer(player, self)

			if not player.isHide:
				if self.autoRespawn:
					self.rooms.server.users.respawnMouse(player)

	def removeClient(self, player):
		if self.isFuncorp:
			found = False
			for player2 in self.players.values():
				if player2 != player:
					if player2.isFuncorp:
						found = True
						break
			if not found:
				for player2 in self.players.values():
					player2.funColor = ""
					player2.funMouseColor = ""
				self.isFuncorp = False
				self.isPublic = False
				self.kickeds = []
				self.rooms.sendLangueMessageToRoom(self, player.langue.lower(), "<CEP>$FunCorpDesactive</CEP>", [])

		self.users.sendPlayerDisconnect(self, player)

		del self.players[self.users.parsePlayerName(player)]

		if len(self.players) > 0:
			noDead = self.rooms.getPlayersNoDead(self)
			if noDead == 0:
				self.startMap()
		else:
			if self.musicTimer != None:
				self.musicTimer.cancel()

			if self.changeTimer != None:
				self.changeTimer.cancel()

			if self.killAfkTimer != None:
				self.killAfkTimer.cancel()

			if self.vampireTimer != None:
				self.vampireTimer.cancel()

			for reac in self.reactors:
				reac.cancel()
				self.reactors.remove(reac)

			if not self.noRemoveRoom:
				self.rooms.removeRoom(self.roomName)

	def startMap(self):
		if self.changeTimer != None:
			self.changeTimer.cancel()

		if self.killAfkTimer != None:
			self.killAfkTimer.cancel()

		if self.vampireTimer != None:
			self.vampireTimer.cancel()

		for reac in self.reactors:
			reac.cancel()
			self.reactors.remove(reac)

		self.lastCodePartie = (self.lastCodePartie + 1) % 255
		self.roundsRunned += 1

		if self.countStats and self.rooms.getPlayersCountIP(self) >= int(self.rooms.server.config["needToStats"]):
			if self.isSurvivor:
				for player in self.players.values():
					if not player.isNewPlayer:
						player.survivorStats[0] += 1

						if player.isShaman:
							count = self.rooms.getDeathCountNoShaman(self)
							player.survivorStats[1] += 1
							player.survivorStats[2] += count

							if 3 in player.missions and count > 0:
								player.missions[3][1] += count

								if player.missions[3][1] >= player.missions[3][2] and not player.missions[3][4]:
									self.users.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", [32])
									self.users.skills.earnExp(player, 32)
									player.missions[3][4] = True
									self.users.inventory.sendNewConsumable(player, 0, 10)
									self.users.inventory.sendNewConsumable(player, 2, 10)
									self.users.inventory.sendNewConsumable(player, 3, 10)

							self.users.skills.earnExp(player, 20, 1)
						else:
							if not player.isDead:
								player.survivorStats[3] += 1
								self.users.skills.earnExp(player, 20, 1)

						if self.currentPerm == 11:
							if not player.isVampire:
								if not player.isDead:
									player.playerScore += 10
									if self.isQuarentine:
										self.users.skills.earnExp(player, 20, 1)
										if not 501.1 in player.titlesList:
											player.titlesList.append(501.1)
											player.titleID = 501.1
											self.users.sendUnlockedTitle(player)
											self.users.sendTitleList(player)
											self.users.sendChangeTitle(player)
							else:
								if not player.isDead:
									if self.isQuarentine:
										self.users.skills.earnExp(player, 10, 1)

			elif self.isRacing:
				for player in self.players.values():
					if not player.isNewPlayer:
						player.racingStats[0] += 1

						if player.hasEnter:
							player.racingStats[1] += 1

							if player.currentPlace <= 3:
								player.racingStats[2] += 1
								if player.currentPlace == 1:
									player.racingStats[3] += 1

			else:
				if self.currentShamanName != "":
					if self.currentShamanName in self.players:
						player = self.players[self.currentShamanName]
						count = self.holesType[0] + self.holesType[1] + self.holesType[3]
						if count > 0:
							player.seasonCheeseCount += count

							if player.shamanType == 1:
								player.hardModeSaves += count
								self.users.checkShamanHardSavesTitleUnlocked(player)
							elif player.shamanType == 2:
								player.divineModeSaves += count
								self.users.checkShamanDivineSavesTitleUnlocked(player)
							else:
								player.shamanSaves += count
								self.users.checkShamanSavesTitleUnlocked(player)
						self.users.skills.earnExp(player, 20 * count, count)
						for player2 in self.players.values():
							self.users.sendOldPacket(player2.channel, [8, 17], [self.users.parsePlayerName(player), count])

				if self.currentShamanName2 != "":
					if self.currentShamanName2 in self.players:
						player = self.players[self.currentShamanName2]
						count = self.holesType[0] + self.holesType[2] + self.holesType[3]
						if count > 0:
							player.seasonCheeseCount += count
							
							if player.shamanType == 1:
								player.hardModeSaves += count
								self.users.checkShamanHardSavesTitleUnlocked(player)
							elif player.shamanType == 2:
								player.divineModeSaves += count
								self.users.checkShamanDivineSavesTitleUnlocked(player)
							else:
								player.shamanSaves += count
								self.users.checkShamanSavesTitleUnlocked(player)
							self.users.checkShamanSavesTitleUnlocked(player)
						self.users.skills.earnExp(player, 20 * count, count)
						for player2 in self.players.values():
							self.users.sendOldPacket(player2.channel, [8, 17], [self.users.parsePlayerName(player), count])

		if self.isQuarentine:
			if self.rooms.getPlayersNoVampCount(self) > 0:
				for player2 in self.players.values():
					if player2.isNewPlayer and len(list(self.players)) == 1:
						break
					self.users.sendMessage2(player2.channel, "<VP>Vitória dos ratos!</VP>")
			else:
				for player2 in self.players.values():
					if player2.isNewPlayer and len(list(self.players)) == 1:
						break
					self.users.sendMessage2(player2.channel, "<R>Vitória dos vampiros!</R>")

		for player in self.players.values():
			if not player.isDead and not player.isNewPlayer:
				self.users.sendPlayerDied(player, True)
				
			if player.isShaman:
				player.playerScore = 0

			if player.isNewPlayer:
				player.isNewPlayer = False
			else:
				if self.rooms.getPlayersCountIP(self) >= int(self.rooms.server.config["needToFirst"]):
					player.roundsPlayed += 1

		self.rooms.resetMap(self)
		self.rooms.selectMap(self)

		if self.leveTest:
			self.leveTest = False

		if self.currentMap in [108, 109, 110, 111, 112, 113]:
			self.catchTheCheeseMap = True

		if self.currentPerm in [7, 11]:
			self.isNoShamanMap = True

			if self.currentPerm == 11:
				self.vampiresRand = self.rooms.randVampire(self)

		if not self.noShaman and not self.isNoShamanMap:
			if self.currentMap in self.rooms.doubleShamanMaps and self.rooms.getPlayersCount(self) >= 2:
				self.isDoubleShaman = True
				self.rooms.getDoubleShamanCode(self)
				self.lastShamanName = self.currentShamanName
				self.lastShamanName2 = self.currentShamanName2
			else:
				self.isDoubleShaman = False
				self.rooms.getShamanCode(self)
				self.lastShamanName = self.currentShamanName
				self.lastShamanName2 = ""

			if not self.noShamanSkills:
				if 0 in self.currentShamanSkills:
					self.addTime += self.currentShamanSkills[0] * 5
				if 0 in self.currentSecondShamanSkills:
					self.addTime += self.currentSecondShamanSkills[0] * 5

		self.rooms.getSyncCode(self)

		self.isCurrentlyPlay = True

		for player in self.players.values():
			self.users.resetPlayer(player)

		for player in self.players.values():
			self.users.startPlayer(player, self)

		if self.showPWinner:
			self.showPWinner = False
			self.users.sendLangueMessageToRoom(self, "", "$MeilleurJoueur", [self.users.parsePlayerName(player)])

		if self.isRacing or self.isDefilante or self.isQuarentine:
			self.roundsCount = (self.roundsCount + 1) % 10
			player = self.rooms.getHighestScore(self)
			self.rooms.sendAll(self, [5, 1], ByteArray().writeByte(self.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
			if self.roundsCount == 9:
				self.rooms.resetAllScores(self)
				self.showPWinner = True

		if not self.noRecords:
			if self.currentMap in self.rooms.records:
				record = self.rooms.records[self.currentMap]
				self.users.sendLangueMessageToRoom(self, "", "$MessageRecord", [str(record["Time"])[:5], record["playerName"]])

		if self.killAllAfk:
			self.killAfkTimer = threading.Timer(30, self.akillAllAfk)
			self.killAfkTimer.start()

		if self.isSurvivor and self.currentPerm == 11 or self.isQuarentine:
			self.vampireTimer = threading.Timer(10, self.sendTransformAllVampire)
			self.vampireTimer.start()

		self.changeTimer = threading.Timer(self.roundTime + self.addTime + 3 if self.count3Seconds else 0, self.startMap)
		self.changeTimer.start()

		if self.count3Seconds:
			for player in self.players.values():
				self.users.sendMapAccess(player.channel, 1)
			t = threading.Timer(3, self.send3SecondsAll)
			self.reactors.append(t)
			t.start()

	def getPlayersNoDead(self):
		noDead = 0
		for player in self.players.values():
			if not player.isDead:
				noDead += 1
		return noDead

	def akillAllAfk(self):
		for player in self.players.values():
			if player.isAfk and not player.isDead and not player.isNewPlayer:
				self.users.sendPlayerDied(player, True)

		noDead = self.getPlayersNoDead()
		if noDead == 0:
			self.startMap()

	def sendTransformAllVampire(self):
		self.vampireSelected = True
		
		for player in self.vampiresRand:
			self.vampiresList.append(player.playerCode)
			self.rooms.sendAll(self, [8, 66], ByteArray().writeInt(player.playerCode).writeInt(-1).toByteArray())
			
			if self.isQuarentine:
				for player2 in self.players.values():
					self.users.sendMessage2(player2.channel, "<R><b>{}</b> foi infectado!</R>".format(self.users.parsePlayerName(player)))

	def send3SecondsAll(self):
		for player in self.players.values():
			self.users.sendMapAccess(player.channel, 0)