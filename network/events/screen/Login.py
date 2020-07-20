import re, threading, time
from server.helpers.String import *
from network.packet.ByteArray import *

class Login:
	C, CC = 26, 8

	@staticmethod
	def parse(users, channel, packet, packetID):
		player = channel.player

		packet = users.packetManage.packetEncryption.identification(packet, packetID)
		playerName = packet.readUTF().capitalize()
		password = packet.readUTF()
		player.link = packet.readUTF()
		startRoom = packet.readUTF()
		loginXor = packet.readInt()
		dataKey = packet.readByte()

		calcXor = player.loginXor
		for key in users.server.config["protection"]["loginKeys"]:
			calcXor = calcXor ^ key

		#if loginXor != calcXor:
		#	return
		if playerName in users.players:
			users.sendPacket(channel, [26, 12], ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
		else:
			#if not player.langue.lower() in ["br", "es"]:
			#	users.sendOldPacket(channel, [26, 18], [str(0 * 3600000), "This server is Spain/Brazilian. Please, if you want to play, select the ES or BR community."])
			#	channel.close_connection()
			#	return

			if(password != ""):
				if "@" in playerName.lower():
					if playerName.lower() in users.server.cache.usersByEmail:
						usersList = users.server.cache.usersByEmail[playerName.lower()]
						if len(usersList) == 1:
							playerName = usersList[0]
						else:
							users.sendPacket(channel, [26, 12], ByteArray().writeByte(11).writeUTF("¤".join(usersList)).writeUTF("").toByteArray())
							return
					else:
						users.sendPacket(channel, [26, 12], ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray())
						return

				if not "#" in playerName:
					playerName = "{}#0000".format(playerName)

				if playerName in users.players:
					users.sendPacket(channel, [26, 12], ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
					return
					
				pool = users.server.database.execute("SELECT * FROM users WHERE playerName = %s AND playerTag = %s AND Hash = %s", (playerName.split("#")[0], playerName.split("#")[1], password))
				results = users.server.database.fetchone(pool)
				if results != None:
					if channel.ipAddress in users.server.ipBans:
						ban = users.server.ipBans[channel.ipAddress]
						h = users.server.getHoursDiff(ban["time"])
						if h > 0:
							users.sendOldPacket(channel, [26, 18], [str(h * 3600000), ban["reason"]])
							channel.close_connection()
							return
						else:
							del users.server.ipBans[channel.ipAddress]
							
					if playerName in users.server.bans:
						ban = users.server.bans[playerName]
						h = users.server.getHoursDiff(ban["time"])
						if h > 0:
							users.sendOldPacket(channel, [26, 18], [str(h * 3600000), ban["reason"]])
							channel.close_connection()
							return
						else:
							del users.server.bans[playerName]

					player.isLogged = True
					player.playerName = results["playerName"]
					player.playerTag = results["playerTag"]
					player.playerID = results["playerID"]
					player.privLevel = results["Privilege"]
					player.regDate = results["regDate"]
					player.playingTime = results["playingTime"]
					player.gender = results["gender"]
					player.shamanLevel = results["shamanLevel"]
					player.shamanExp = results["shamanExp"]
					player.shamanExpNext = results["shamanExpNext"]
					player.titleID = float(results["titleID"])
					player.cheeseCount = results["cheeseCount"]
					player.firstCount = results["firstCount"]
					player.bootcampCount = results["bootcampCount"]
					player.shamanSaves = results["shamanSaves"]
					player.shamanCheeses = results["shamanCheeses"]
					player.hardModeSaves = results["hardModeSaves"]
					player.divineModeSaves = results["divineModeSaves"]
					player.marriage = results["marriage"]
					player.survivorStats = list(map(int, list(filter(str, results["survivorStats"].split(",")))))
					player.racingStats = list(map(int, list(filter(str, results["racingStats"].split(",")))))
					player.titlesList = list(map(float, list(filter(str, results["titlesList"].split(",")))))
					player.shopCheeses = results["shopCheeses"]
					player.shopFraises = results["shopFraises"]
					skills = list(filter(str, results["playerSkills"].split(";")))
					for skill in skills:
						skillID = int(skill.split(",")[0])
						count = int(skill.split(",")[1])
						player.playerSkills[skillID] = count
					player.shopItems = list(filter(str, results["shopItems"].split(",")))
					player.shamanItems = list(filter(str, results["shamanItems"].split(",")))
					player.playerLook = results["playerLook"]
					player.shamanLook = results["shamanLook"]
					player.friendsList = list(filter(str, results["friendsList"].split(",")))
					player.ignoredsList = list(filter(str, results["ignoredsList"].split(",")))
					player.lastLogin = results["lastLogin"]
					player.chats = list(filter(str, results["chats"].split(",")))
					player.colorNick = results["colorNick"]
					player.roundsPlayed = results["roundsPlayed"]
					player.shopBadges = list(filter(str, results["shopBadges"].split(",")))
					player.isVip = bool(results["isVip"])
					player.shamanType = results["shamanType"]
					player.clothes = list(filter(str, results["clothes"].split("|")))
					player.mouseColor = results["mouseColor"]
					player.karmas = results["karmas"]
					player.referrals = results["referrals"]
					player.seasonFirstCount = results["seasonFirstCount"]
					player.seasonCheeseCount = results["seasonCheeseCount"]
					player.seasonSavesCount = results["seasonSavesCount"]
					consumables = list(filter(str, results["playerConsumables"].split(";")))
					for consumable in consumables:
						id = int(consumable.split(",")[0])
						count = int(consumable.split(",")[1])
						player.playerConsumables[id] = count
					for missionID in list(filter(str, results["missions_completed"].split(","))):
						missionID = int(missionID)
						if missionID in player.missions:
							player.missions[missionID][1] = player.missions[missionID][2]
							player.missions[missionID][4] = True
					player.isFuncorp = int(results["isFuncorp"])

					player.playerCode = channel.server.users.getPlayerCode()
					users.players[users.parsePlayerName(channel.player)] = channel.player

					if len(list(users.players)) > users.server.config["record_players_online"]:
						users.server.config["record_players_online"] = len(list(users.players))

					if player.privLevel >= 9:
						player.privsList.append(10)
						player.titlesList.append(440.1)
						player.titlesList.append(442.1)
						player.titlesList.append(444.1)
						player.titlesList.append(445.1)
						player.titlesList.append(446.1)
						player.titlesList.append(447.1)
						player.titlesList.append(448.1)
						player.titlesList.append(449.1)
						player.titlesList.append(450.1)
						player.titlesList.append(451.1)
						player.titlesList.append(452.1)
						player.titlesList.append(453.1)
					if player.privLevel >= 4:
						player.privsList.append(5)
					if player.privLevel >= 2:
						player.privsList.append(3)
					if player.isFuncorp:
						player.privsList.append(13)
					if player.isLuacrew:
						player.privsList.append(12)
					if player.isMapcrew:
						player.privsList.append(11)
 
					if channel.geoIP.matched:
						pool = users.server.database.execute("INSERT INTO geoip (playerName, ip, country_code, country_name, region_code, region_name, city, zip_code, time_zone, latitude, longitude, metro_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (users.parsePlayerName(channel.player), channel.ipAddress, channel.geoIP.json["country_code"], channel.geoIP.json["country_name"], channel.geoIP.json["region_code"], channel.geoIP.json["region_name"], channel.geoIP.json["city"], channel.geoIP.json["zip_code"], channel.geoIP.json["time_zone"], channel.geoIP.json["latitude"], channel.geoIP.json["longitude"], channel.geoIP.json["metro_code"]))
						users.server.database.commitAll()

					pool = users.server.database.execute("INSERT INTO transformice_loginlog (playerName, ip, date) VALUES (%s, %s, %s)", (users.parsePlayerName(player), channel.ipAddress, time.ctime()))
					users.server.database.commitAll()
						
					player.connectedTime = users.server.getTime()
					users.sendPlayerIdentification(channel, player.playerID, users.parsePlayerName(channel.player), player.playingTime, results["langueID"], player.playerCode, player.playerName[:1] == "*", player.privsList)
					users.sendPacket(channel, [100, 6], ByteArray().writeShort(0).toByteArray())
					users.server.tribulle.joinTribulle(channel.player)

					if player.isVip:
						if not "V.I.P" in player.chats:
							player.chats.append("V.I.P")
					else:
						if "V.I.P" in player.chats:
							player.chats.remove("V.I.P")
							
					for chatName in player.chats:
						if not chatName in users.server.chats:
							users.server.chats[chatName] = []
						users.server.chats[chatName].append(users.parsePlayerName(channel.player))
						users.server.tribulle.sendChatJoin(channel.player, chatName)

					users.skills.sendShamanSkills(channel, False)
					users.skills.sendExp(channel, player.shamanLevel, player.shamanExp, player.shamanExpNext)
					users.shop.sendShamanItems(channel.player)
					users.sendInventoryConsumables(channel)
					users.sendPacket(channel, [28, 2], ByteArray().writeInt(users.server.getTime()).toByteArray())
					users.sendPacket(channel, [144, 5], ByteArray().writeBoolean(True).toByteArray())
					users.sendPacket(channel, [28, 13], ByteArray().writeBoolean(True).toByteArray())
					
					if player.shamanSaves >= 50:
						users.sendShamanType(channel.player, player.shamanType, True)
						
					users.inventory.openInventory(player)
					#users.openMissions(player)
					#users.sendLangueMessage(channel, player.langue.lower(), "$MessageHelp", [])
					users.sendLangueMessage(channel, player.langue.lower(), "$MessageMission", [])

					users.sendMessageToPriv(3, "{} just connected.".format(users.parsePlayerName(channel.player)), False)

					if player.privLevel >= 5:
						for player2 in users.players.values():
							if player2.privLevel >= 2:
								users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(3).writeUTF(player.langue).writeUTF("{} just connected.".format(users.parsePlayerName(channel.player))).writeBoolean(True).writeBoolean(False).writeByte(0).toByteArray())

					if player.privLevel >= 2:
						for player2 in users.players.values():
							if player2.privLevel >= 2 and player2 != channel.player:
								users.sendPacket(channel, [6, 10], ByteArray().writeByte(3).writeUTF(player.langue).writeUTF("{} : {}".format(users.parsePlayerName(player2), player2.room.roomName)).writeBoolean(True).writeBoolean(False).writeByte(0).toByteArray())

					if player.privLevel == 2:
						for player2 in users.players.values():
							if player2.privLevel >= 2:
								users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(2).writeUTF(player.langue).writeUTF("{} just connected.".format(users.parsePlayerName(channel.player))).writeBoolean(True).writeBoolean(False).writeByte(0).toByteArray())

					if player.privLevel >= 2:
						for player2 in users.players.values():
							if player2.privLevel == 2 and player2 != channel.player:
								users.sendPacket(channel, [6, 10], ByteArray().writeByte(2).writeUTF(player.langue).writeUTF("{} : {}".format(users.parsePlayerName(player2), player2.room.roomName)).writeBoolean(True).writeBoolean(False).writeByte(0).toByteArray())

					users.enterRoom(channel.player, users.server.rooms.getRecommendRoom(users.server.langues.getLangue(player.langueID), startRoom))
					if player.isStandAlone and not player.missions[52][4]:
						users.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", ["32"])
						users.skills.earnExp(player, 32)
						player.missions[52][4] = True
						player.missions[52][1] += 1
						player.titlesList.append(552.1)
						player.titleID = 552.1
						users.sendUnlockedTitle(player)
						users.sendTitleList(player)
						users.sendChangeTitle(player)
						users.inventory.sendNewConsumable(player, 0, 10)
						users.inventory.sendNewConsumable(player, 2, 10)
						users.inventory.sendNewConsumable(player, 3, 10)
				else:
					users.sendPacket(channel, [26, 12], ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray())
			else:
				users.sendPacket(channel, [26, 12], ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray())