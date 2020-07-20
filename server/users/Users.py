import zlib, json, threading
from network.packet.ByteArray import *

class Users:
	def __init__(self, server):
		self.players = {}
		self.season_ranking = {"first": [], "cheese": [], "saves": []}

		self.lastPlayerCode = 1

		self.server = server
		self.commands = None
		self.skills = None
		self.shop = None
		self.inventory = None
		self.missions = None
		self.packetManage = None

		self.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
		self.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
		self.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
		self.firstTitleList = {1:9.1, 10:10.1, 100:11.1, 200:12.1, 300:42.1, 400:43.1, 500:44.1, 600:45.1, 700:46.1, 800:47.1, 900:48.1, 1000:49.1, 1100:50.1, 1200:51.1, 1400:52.1, 1600:53.1, 1800:54.1, 2000:55.1, 2200:56.1, 2400:57.1, 2600:58.1, 2800:59.1, 3000:60.1, 3200:61.1, 3400:62.1, 3600:63.1, 3800:64.1, 4000:65.1, 4500:66.1, 5000:67.1, 5500:68.1, 6000:69.1, 7000:231.1, 8000:232.1, 9000:233.1, 10000:70.1, 12000:224.1, 14000:225.1, 16000:226.1, 18000:227.1, 20000:202.1, 25000:228.1, 30000:229.1, 35000:230.1, 40000:71.1}
		self.cheeseTitleList = {5:5.1, 20:6.1, 100:7.1, 200:8.1, 300:35.1, 400:36.1, 500:37.1, 600:26.1, 700:27.1, 800:28.1, 900:29.1, 1000:30.1, 1100:31.1, 1200:32.1, 1300:33.1, 1400:34.1, 1500:38.1, 1600:39.1, 1700:40.1, 1800:41.1, 2000:72.1, 2300:73.1, 2700:74.1, 3200:75.1, 3800:76.1, 4600:77.1, 6000:78.1, 7000:79.1, 8000:80.1, 9001:81.1, 10000:82.1, 14000:83.1, 18000:84.1, 22000:85.1, 26000:86.1, 30000:87.1, 34000:88.1, 38000:89.1, 42000:90.1, 46000:91.1, 50000:92.1, 55000:234.1, 60000:235.1, 65000:236.1, 70000:237.1, 75000:238.1, 80000:93.1}
		self.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187, 2290:189, 2291:191, 2292:192, 2293:194, 2294:195, 2295:196, 2296:197, 2297:199, 2298:200, 2299:201, 230100:203, 230101:204, 230102:205, 230103:206, 230104:207, 230105:208, 230106:210, 230107:211, 230108:212, 230110: 214, 230111: 215, 230112: 216, 230113: 217, 230114: 220, 230115: 222, 230116: 223, 230117: 224, 230118: 225, 230119: 226, 230120: 227, 230121: 228, 230122: 229, 230123: 231, 230124: 232, 230125: 233, 230126: 234, 230127: 235, 230128: 236, 230129: 237, 230130: 238, 230131: 239, 230132: 241, 230133: 242, 230134: 243, 230135: 244, 230136: 245, 230137: 246, 230138: 247}
		self.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
		self.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}

		self.removeNoConnectedAccounts()
		
	def getPlayerCode(self):
		self.lastPlayerCode += 1
		return self.lastPlayerCode
		
	def updateDatabase(self, player):
		skills = []
		for skillID, count in player.playerSkills.items():
			skills.append(f"{skillID},{count}")
		consumables = []
		for consumable, count in player.playerConsumables.items():
			consumables.append(f"{consumable},{count}")
		missions_completed = []
		for id, values in player.missions.items():
			if values[4] == 1:
				missions_completed.append(str(id))
		if player.privLevel >= 9:
			player.titlesList.remove(440.1)
			player.titlesList.remove(442.1)
			player.titlesList.remove(444.1)
			player.titlesList.remove(445.1)
			player.titlesList.remove(446.1)
			player.titlesList.remove(447.1)
			player.titlesList.remove(448.1)
			player.titlesList.remove(449.1)
			player.titlesList.remove(450.1)
			player.titlesList.remove(451.1)
			player.titlesList.remove(452.1)
			player.titlesList.remove(453.1)
		pool = self.server.database.execute("UPDATE users SET Privilege = %s, playingTime = %s, gender = %s, titleID = %s, cheeseCount = %s, firstCount = %s, bootcampCount = %s, shamanLevel = %s, shamanExp = %s, shamanExpNext = %s, shamanSaves = %s, shamanCheeses = %s, hardModeSaves = %s, divineModeSaves = %s, survivorStats = %s, racingStats = %s, playerSkills = %s, marriage = %s, titlesList = %s, shopItems = %s, shamanItems = %s, playerLook = %s, shamanLook = %s, friendsList = %s, ignoredsList = %s, lastLogin = %s, chats = %s, colorNick = %s, roundsPlayed = %s, shopBadges = %s, isVip = %s, shamanType = %s, clothes = %s, mouseColor = %s, karmas = %s, referrals = %s, missions_completed = %s, seasonFirstCount = %s, seasonCheeseCount = %s, seasonSavesCount = %s, playerConsumables = %s where playerID = %s", (player.privLevel, player.playingTime + int(self.server.getTime() - player.connectedTime), player.gender, str(player.titleID), player.cheeseCount, player.firstCount, player.bootcampCount, player.shamanLevel, player.shamanExp, player.shamanExpNext, player.shamanSaves, player.shamanCheeses, player.hardModeSaves, player.divineModeSaves, ','.join(map(str, player.survivorStats)), ','.join(map(str, player.racingStats)), ";".join(skills), player.marriage, ",".join(list(map(str, player.titlesList))), ",".join(player.shopItems), ",".join(player.shamanItems), player.playerLook, player.shamanLook, ",".join(player.friendsList), ",".join(player.ignoredsList), player.lastLogin, ",".join(player.chats), player.colorNick, player.roundsPlayed, ",".join(list(map(str, player.shopBadges))), int(player.isVip), player.shamanType, "|".join(map(str, player.clothes)), player.mouseColor, player.karmas, player.referrals, ",".join(missions_completed), player.seasonFirstCount, player.seasonCheeseCount, player.seasonSavesCount, ";".join(consumables), player.playerID))
		self.server.database.commitAll()
		
	def parsePlayerName(self, player):
		return "{}#{}".format(player.playerName, player.playerTag)

	def checkPlayerNameExist(self, playerName):
		found = False
		for email, accounts in self.server.cache.usersByEmail.items():
			if playerName in accounts:
				found = True
				break
		return found

	def sendPacket(self, channel, identifiers, data):
		if channel.isClosed:
			return
		channel.packetID = (channel.packetID + 1) % 255
		packet = ByteArray()
		length = len(data) + 2
		calc1 = length >> 7
		while calc1 != 0:
			packet.writeUnsignedByte(((length & 127) | 128))
			length = calc1
			calc1 = calc1 >> 7
		packet.writeByte((length & 127)).writeUnsignedByte(identifiers[0]).writeUnsignedByte(identifiers[1]).writeBytes(data)
		channel.writeData(packet.toByteArray())

	def sendOldPacket(self, channel, identifiers, values):
		if channel.isClosed:
			return
		self.sendPacket(channel, [1, 1], ByteArray().writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + list(map(str, filter(str, values)))))).toByteArray())

	def sendPlayerIdentification(self, channel, playerID, playerName, playingTime, langueID, playerCode, isGuest, privs):
		packet = ByteArray().writeInt(playerID).writeUTF(playerName).writeInt(playingTime).writeByte(langueID).writeInt(playerCode).writeBoolean(not isGuest).writeByte(len(privs))
		for priv in privs:
			packet.writeByte(priv)
		self.sendPacket(channel, [26, 2], packet.writeBoolean(True).toByteArray()) 

	def sendInventoryConsumables(self, channel):
		packet = ByteArray().writeShort(0) # size
		self.sendPacket(channel, [31, 1], packet.toByteArray())

	def enterRoom(self, player, roomName):
		channel = player.channel

		roomName = roomName.replace("<", "&lt;")

		if not roomName[:1] == "*":
			if len(roomName) > 3 and roomName[2] == "-" and self.server.langues.checkExistLangueStr(roomName[:2]):
				roomName = "{}-{}".format(roomName[:2].lower(), roomName[3:])
			else:
				roomName = "{}-{}".format(player.langue.lower(), roomName)

		if roomName in list(self.server.rooms.rooms):
			if self.parsePlayerName(player) in self.server.rooms.rooms[roomName].kickeds:
				return

		if player.room != None:
			if roomName == player.room.roomName:
				return

			self.server.rooms.leaveRoom(player, player.room.roomName)

		self.sendRoomGameMode(channel, roomName)
		self.sendEnterRoom(channel, roomName)
		self.server.rooms.joinRoom(player, roomName)
		self.sendOldPacket(channel, [5, 7], player.room.anchors)
		self.sendPacket(channel, [29, 1], b"")

		if player.room.isMusic:
			if len(player.room.musicList) == 0:
				self.sendPacket(channel, [5, 72], ByteArray().writeUTF("").writeUTF("").writeShort(0).writeUTF("").toByteArray())
			else:
				m = list(player.room.musicList)[0]
				music = player.room.musicList[m]
				self.sendPacket(channel, [5, 72], ByteArray().writeUTF(music["items"][0]["id"]).writeUTF(music["items"][0]["snippet"]["title"]).writeShort(int(self.server.getTime() - player.room.room.musicStartedTime)).writeUTF(m).toByteArray())

		if player.room.isFuncorp:
			self.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", ["32"])

		if player.room.isQuarentine:
			self.sendMessage2(channel, "<J>(!)</J> <N>Bem-vindo(a) a sala <J>Quarentena</J>. Sua missão como rato é sobreviver até o tempo acabar!</VP>")

		for playerCode in player.room.vampiresList:
			self.sendPacket(channel, [8, 66], ByteArray().writeInt(playerCode).writeInt(-1).toByteArray())
		
		for friend in self.server.tribulle.getFriendsClass(player):
			self.server.tribulle.sendFriendChangedRoom(player, friend)

		if player.seasonMessage:
			self.sendAddTextArea(channel, 41, "<br><p align='center'><N><a href='event:openSeasonMessage'><B>Ranking da Temporada</B></a></N></p>", 620, 13, 175, 35, int("324650", 16), 0, 100)
		else:
			self.sendSeasonRanking(channel)
			player.seasonMessage = True

	def sendRoomGameMode(self, channel, roomName):
		roomName = roomName.lower()
		self.sendPacket(channel, [7, 1], ByteArray().writeByte(4 if "madchees" in roomName else 0).toByteArray())
		self.sendPacket(channel, [7, 30], ByteArray().writeByte(2 if "bootcamp" in roomName else 3 if "vanilla" in roomName else 8 if "survivor" in roomName else 9 if "racing" in roomName else 10 if "defilante" in roomName else 11 if "music" in roomName else 16 if "village" in roomName else 1).toByteArray())

	def sendEnterRoom(self, channel, roomName):
		self.sendPacket(channel, [5, 21], ByteArray().writeBoolean(roomName[:1] in ["*", "\x03"]).writeUTF(roomName).toByteArray())

	def getPlayerData(self, player):
		return ByteArray().writeUTF(self.parsePlayerName(player)).writeInt(player.playerCode).writeBoolean(player.isShaman).writeByte(int(player.isDead)).writeShort(player.playerScore).writeBoolean(player.hasCheese).writeShort(int(str(player.titleID).split(".")[0])).writeByte(int(str(player.titleID).split(".")[1])).writeByte(player.gender).writeUTF("0").writeUTF(player.playerLook).writeBoolean(True).writeInt(int(player.funMouseColor, 16) if len(player.funMouseColor) > 0 else int(player.mouseColor, 16)).writeInt(int(player.shamanColor, 16)).writeInt(0).writeInt(int(player.funColor, 16) if player.funColor != "" else int(player.colorNick, 16) if player.colorNick != "" else -1).toByteArray()

	def sendPlayerList(self, channel, room):
		playersList = self.server.rooms.getPlayersList(room)
		packet = ByteArray()
		packet.writeShort(len(playersList))
		for playerData in playersList:
			packet.writeBytes(playerData)
		self.sendPacket(channel, [144, 1], packet.toByteArray())

	def resetPlayer(self, player):
		player.isDead = False
		player.hasCheese = False
		player.isAfk = True
		player.isSync = False
		player.isMovingRight = False
		player.isMovingLeft = False
		player.isAfk = True
		player.posX = 0
		player.posY = 0
		player.velX = 0
		player.velY = 0
		player.iceCount = 0
		player.isVampire = False
		player.hasEnter = False
		player.currentPlace = False
		player.canShamanRespawn = False
		player.isOpportunist = False
		player.desintegration = False
		
	def startPlayer(self, player, room):
		channel = player.channel

		player.playerStartTimeMillis = self.server.getTime()

		self.sendPacket(channel, [5, 2], ByteArray().writeInt(0 if room.isEditeur else room.currentMap).writeShort(self.server.rooms.getPlayersCount(room)).writeUnsignedByte(room.lastCodePartie).writeShort(0).writeUTF(zlib.compress(room.EMapXML.encode() if room.isEditeur else room.currentXML.encode())).writeUTF("" if room.isEditeur else room.currentName).writeByte(0 if room.isEditeur else room.currentPerm).writeBoolean(room.currentInverted).toByteArray())

		if player.playerCode == room.currentShamanCode or player.playerCode == room.currentShamanCode2:
			player.isShaman = True
		else:
			player.isShaman = False

		if player.playerCode == room.currentSyncCode:
			player.isSync = True
		else:
			player.isSync = False

		if player.isShaman and not player.room.noShamanSkills:
			self.skills.getShamanSkills(player)

		if player.room.currentShamanName != "" and not player.room.noShamanSkills:
			self.skills.getPlayerSkills(player, player.room.currentShamanSkills)

		if player.room.currentShamanName2 != "" and not player.room.noShamanSkills:
			self.skills.getPlayerSkills(player, player.room.currentSecondShamanSkills)
			
		self.sendPlayerList(channel, room)

		if room.catchTheCheeseMap and not room.noShamanSkills:
			self.sendOldPacket(channel, [8, 23], [room.currentShamanCode])
			self.sendPacket(channel, [144, 6], ByteArray().writeInt(room.currentShamanCode).writeBoolean(True).toByteArray())
			if not room.currentMap in [108, 109]:
				self.sendPacket(channel, [8, 11], ByteArray().writeInt(room.currentShamanCode).writeInt(room.currentShamanCode2).writeByte(room.currentShamanType if not room.isSurvivor else 0).writeByte(room.currentShamanType2 if not room.isSurvivor else 0).writeShort(room.currentShamanLevel).writeShort(room.currentShamanLevel2).writeShort(room.currentShamanBadge).writeShort(room.currentShamanBadge2).toByteArray())
		else:
			self.sendPacket(channel, [8, 11], ByteArray().writeInt(room.currentShamanCode).writeInt(room.currentShamanCode2).writeByte(room.currentShamanType if not room.isSurvivor else 0).writeByte(room.currentShamanType2 if not room.isSurvivor else 0).writeShort(room.currentShamanLevel).writeShort(room.currentShamanLevel2).writeShort(room.currentShamanBadge).writeShort(room.currentShamanBadge2).toByteArray())

		self.sendSync(channel, room.currentSyncCode)
		self.sendRoundTime(channel, (self.server.rooms.getRoundTime(room) + room.gameStartTimeMillis) - self.server.getTime())

		if room.isCurrentlyPlay:
			self.sendMapAccess(channel, 0)
		else:
			self.sendMapAccess(channel, 1)

		if room.isSurvivor and player.isShaman:
			self.sendPacket(channel, [8, 39], ByteArray().writeBoolean(True).toByteArray())

		if room.currentMap in [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211] and not player.isShaman:
			if not room.isRacing and not room.isDefilante and not room.isBootcamp:
				self.sendTransformation(player.channel, True)

	def respawnMouse(self, player):
		room = player.room

		player.playerStartTimeMillis = self.server.getTime()

		player.isDead = False
		player.hasCheese = False

		self.server.rooms.sendAll(room, [144, 2], ByteArray().writeBytes(self.getPlayerData(player)).writeBoolean(False).writeBoolean(True).toByteArray())

	def respawnSpecific(self, player):
		player.playerStartTimeMillis = self.server.getTime()
		self.resetPlayer(player)
		self.respawnMouse(player)

	def sendPlayerDied(self, player, afkKill=False):
		room = player.room
		player.isDead = True
		player.hasCheese = False

		if self.server.rooms.getPlayersCount(room) >= 2:
			player.playerScore += 1

		noDead = room.rooms.getPlayersNoDead(room)
		self.server.rooms.sendAllOld(room, [8, 5], [player.playerCode, noDead, player.playerScore, "0"])

		if not afkKill:
			if noDead < 1 or room.catchTheCheeseMap or player.isAfk:
				player.canShamanRespawn = False

			if player.canShamanRespawn or room.autoRespawn:
				if player.canShamanRespawn:
					player.isDead = False
					player.isAfk = False
					player.hasCheese = False
					player.hasEnter = False
					player.canShamanRespawn = False
					player.playerStartTimeMillis = self.server.getTime()
					self.server.rooms.sendAll(room, [144, 2], ByteArray().writeBytes(self.getPlayerData(player)).writeBoolean(False).writeBoolean(True).toByteArray())
					for player2 in room.players.values():
						self.sendPacket(player2.channel, [8, 11], ByteArray().writeInt(player.playerCode).writeInt(0).writeByte(player.shamanType).writeByte(0).writeShort(player.shamanLevel).writeShort(0).writeShort(player.Badge).writeShort(0).toByteArray())
				else:
					self.respawnMouse(player)
			else:
				if noDead == 0:
					room.startMap()
				else:
					t = room.roundTime - int(self.server.getTime() - room.gameStartTimeMillis)
					if player.isShaman:
						if not room.isDoubleShaman:
							if t > 25:
								room.rooms.changeMapTime(room, 20)
								
					if player.room.noShaman:
						if self.server.rooms.getPlayersCount(player.room) < 4:
							room.rooms.changeMapTime(room, 20)

	def sendRoundTime(self, channel, seconds):
		self.sendPacket(channel, [5, 22], ByteArray().writeShort(seconds).toByteArray())

	def sendPlayerDisconnect(self, room, player):
		self.server.rooms.sendAllOld(room, [8, 7], [player.playerCode])

	def sendSync(self, channel, playerCode):
		if channel.player.room.currentMap != 1:
			self.sendOldPacket(channel, [8, 21], [playerCode, ""])
		else:
			self.sendOldPacket(channel, [8, 21], [playerCode])

	def sendTransformation(self, channel, enable):
		self.sendPacket(channel, [27, 10], ByteArray().writeBoolean(enable).toByteArray())

	def sendMapAccess(self, channel, value):
		self.sendPacket(channel, [5, 10], ByteArray().writeByte(value).toByteArray())

	def sendMessage(self, channel, message, toTab=True):
		self.sendPacket(channel, [6, 20], ByteArray().writeBoolean(toTab).writeUTF(message).writeByte(0).writeUTF("").toByteArray())

	def sendMessage2(self, channel, message):
		self.sendPacket(channel, [6, 9], ByteArray().writeUTF(message).toByteArray())

	def sendMessageToPriv(self, priv, message, toTab=True):
		for player in self.players.values():
			if player.privLevel >= priv:
				self.sendMessage(player.channel, message, toTab)

	def sendLangueMessageToRoom(self, room, community, langue, arguments, noPlayer=None):
		for player in room.players.values():
			if player != noPlayer:
				self.sendLangueMessage(player.channel, community, langue, arguments)

	def sendSaveRemainingMiceMessage(self, channel):
		self.sendOldPacket(channel, [8, 18], [])

	def sendGiveCurrency(self, channel, id, count):
		self.sendPacket(channel, [8, 2], ByteArray().writeByte(id).writeByte(count).toByteArray())

	def sendPlaceObject(self, player, room, objectID, code, posX, posY, angle, velX, velY, dur, sendAll):
		if sendAll:
			self.server.rooms.sendAll(room, [5, 20], ByteArray().writeInt(objectID).writeShort(code).writeShort(posX).writeShort(posY).writeShort(angle).writeByte(velX).writeByte(velY).writeByte(dur).writeBytes(self.shop.getShamanItemCustom(player, code)).toByteArray())
		else:
			room.lastObjectID = objectID
			self.server.rooms.sendAllOthers(player, room, [5, 20], ByteArray().writeInt(objectID).writeShort(code).writeShort(posX).writeShort(posY).writeShort(angle).writeByte(velX).writeByte(velY).writeByte(dur).writeBytes(self.shop.getShamanItemCustom(player, code)).toByteArray())

	def sendTransformAllVampire(self, players, room):
		room.vampireSelected = True
		
		for player in players:
			self.server.rooms.sendAll(room, [8, 66], ByteArray().writeInt(player.playerCode).writeInt(-1).toByteArray())

	def chatMessageFilter(self, message):
		for word in self.server.words:
			message = message.replace(word, "***")
		return message

	def filterDisclosure(self, message):
		found = 0
		words = ["trans", "tr4ns", "mic", "m1c", "nov", "n0v", "lin", "l1n", "sit", "s1t", "maic", "ma1c", ".", "/", "new", "n3w", "serv", "s3rv"]
		for word in words:
			if word in message.lower():
				found += 1
		return found >= 3

	def sendChatMessage(self, channel, playerCode, playerName, langueID, message, noAll):
		if noAll:
			self.sendPacket(channel, [6, 6], ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message).toByteArray())
		else:
			self.server.rooms.sendAll(channel.player.room, [6, 6], ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message).toByteArray())

	def sendLangueMessage(self, channel, community, langue, arguments):
		packet = ByteArray().writeUTF(community.lower()).writeUTF(langue).writeByte(len(arguments))
		for argument in arguments:
			packet.writeUTF(argument)
		self.sendPacket(channel, [28, 5], packet.toByteArray())

	def sendMusicVideo(self, room, videoKey, videoTitle, videoTime, videoBy):
		room.rooms.sendAll(room, [5, 72], ByteArray().writeUTF(videoKey).writeUTF(videoTitle).writeShort(videoTime).writeUTF(videoBy).toByteArray())

	def sendProfile(self, to, playerName):
		player = self.players[playerName]
		if player.isHide:
			return
		packet = ByteArray()
		packet.writeUTF(self.parsePlayerName(player))
		packet.writeInt(player.playerID)
		packet.writeInt(player.regDate)
		packet.writeByte(10 if player.privLevel >= 9 else 1 if player.privLevel == 7 else 5 if player.privLevel >= 4 else 3 if player.privLevel >= 2 else 13 if player.isFuncorp else 12 if player.isLuacrew else 11 if player.isMapcrew else 1)
		packet.writeByte(player.gender)
		packet.writeUTF("") # Tribe
		packet.writeUTF(player.marriage)
		packet.writeInt(player.shamanSaves)
		packet.writeInt(player.shamanCheeses)
		packet.writeInt(player.firstCount)
		packet.writeInt(player.cheeseCount)
		packet.writeInt(player.hardModeSaves)
		packet.writeInt(player.bootcampCount)
		packet.writeInt(player.divineModeSaves)
		packet.writeShort(player.titleID)
		packet.writeShort(len(player.titlesList))
		for title in player.titlesList:
			packet.writeShort(int(str(title).split(".")[0]))
			packet.writeByte(int(str(title).split(".")[1]))
		packet.writeUTF(f"{player.playerLook};{player.mouseColor}")
		packet.writeShort(player.shamanLevel)
		packet.writeShort(len(player.shopBadges) * 2)
		badges = list(map(int, player.shopBadges))
		for badge in [120, 121, 122, 123, 124, 125, 126, 127, 145, 42, 54, 55, 0, 1, 6, 7, 9, 16, 17, 18, 28, 29, 30, 33, 34, 35, 46, 47, 50, 51, 57, 58, 59, 64, 65, 69, 71, 73, 129, 130, 131, 132, 133, 134, 139, 142, 144, 147, 153, 154, 158]:
			if badge in badges:
				packet.writeShort(badge)
				packet.writeShort(0)
				badges.remove(badge)
		for badge in badges:
			packet.writeShort(badge)
			packet.writeShort(0)
		stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
		packet.writeByte(len(stats))
		for stat in stats:
			packet.writeUnsignedByte(stat[0])
			packet.writeInt(stat[1])
			packet.writeInt(stat[2])
			packet.writeUnsignedByte(stat[3])
		packet.writeUnsignedByte(len(player.equipedShamanBadge))
		packet.writeUnsignedByte(len(player.shamanBadges))
		for badge in player.shamanBadges:
			packet.writeUnsignedByte(badge)
		packet.writeBoolean(False)
		packet.writeInt(player.adventurePoints)
		self.sendPacket(to.channel, [8, 16], packet.toByteArray())

	def sendTitleList(self, player):
		self.sendOldPacket(player.channel, [8, 15], [player.titlesList])

	def sendUnlockedTitle(self, player):
		self.server.rooms.sendAllOld(player.room, [8, 14], [player.playerCode, int(str(player.titleID).split(".")[0]), int(str(player.titleID).split(".")[1])])

	def sendChangeTitle(self, player):
		self.sendPacket(player.channel, [100, 72], ByteArray().writeUnsignedByte(player.gender).writeShort(int(str(player.titleID).split(".")[0])).toByteArray())

	def checkFirstTitleUnlocked(self, player):
		count = 3
		while count > 0:
			if (player.firstCount - count - 1) in self.firstTitleList:
				titleID = self.firstTitleList[(player.firstCount - count - 1)]
				if not titleID in player.titlesList:
					for l in player.titlesList:
						if int(l) == int(titleID):
							player.titlesList.remove(l)
					player.titlesList.append(titleID)
					player.titleID = titleID
					self.sendUnlockedTitle(player)
					self.sendTitleList(player)
					self.sendChangeTitle(player)
			count -= 1

	def checkCheeseTitleUnlocked(self, player):
		count = 3
		while count > 0:
			if (player.cheeseCount - count - 1) in self.cheeseTitleList:
				titleID = self.cheeseTitleList[(player.cheeseCount - count - 1)]
				if not titleID in player.titlesList:
					for l in player.titlesList:
						if int(l) == int(titleID):
							player.titlesList.remove(l)
					player.titlesList.append(titleID)
					player.titleID = titleID
					self.sendUnlockedTitle(player)
					self.sendTitleList(player)
					self.sendChangeTitle(player)
			count -= 1

	def checkBootcampTitleUnlocked(self, player):
		if player.bootcampCount in self.bootcampTitleList:
			titleID = self.bootcampTitleList[player.bootcampCount]
			if not titleID in player.titlesList:
				for l in player.titlesList:
					if int(l) == int(titleID):
						player.titlesList.remove(l)
				player.titlesList.append(titleID)
				player.titleID = titleID
				self.sendUnlockedTitle(player)
				self.sendTitleList(player)
				self.sendChangeTitle(player)

	def checkShamanSavesTitleUnlocked(self, player):
		if player.shamanSaves in self.shamanTitleList:
			titleID = self.shamanTitleList[player.shamanSaves]
			if not titleID in player.titlesList:
				for l in player.titlesList:
					if int(l) == int(titleID):
						player.titlesList.remove(l)
				player.titlesList.append(titleID)
				player.titleID = titleID
				self.sendUnlockedTitle(player)
				self.sendTitleList(player)
				self.sendChangeTitle(player)

	def checkShamanDivineSavesTitleUnlocked(self, player):
		if player.divineModeSaves in self.divineModeTitleList:
			titleID = self.divineModeTitleList[player.divineModeSaves]
			if not titleID in player.titlesList:
				for l in player.titlesList:
					if int(l) == int(titleID):
						player.titlesList.remove(l)
				player.titlesList.append(titleID)
				player.titleID = titleID
				self.sendUnlockedTitle(player)
				self.sendTitleList(player)
				self.sendChangeTitle(player)

	def checkShamanHardSavesTitleUnlocked(self, player):
		if player.hardModeSaves in self.hardModeTitleList:
			titleID = self.hardModeTitleList[player.hardModeSaves]
			if not titleID in player.titlesList:
				for l in player.titlesList:
					if int(l) == int(titleID):
						player.titlesList.remove(l)
				player.titlesList.append(titleID)
				player.titleID = titleID
				self.sendUnlockedTitle(player)
				self.sendTitleList(player)
				self.sendChangeTitle(player)

	def checkShopTitleUnlocked(self, player):
		if len(player.shopItems) in self.shopTitleList:
			titleID = self.shopTitleList[len(player.shopItems)]
			if not titleID in player.titlesList:
				for l in player.titlesList:
					if int(l) == int(titleID):
						player.titlesList.remove(l)
				player.titlesList.append(titleID)
				player.titleID = titleID
				self.sendUnlockedTitle(player)
				self.sendTitleList(player)
				self.sendChangeTitle(player)

	def playerWin(self, player, holeType, codePartie, monde, distance, holeX, holeY):
		channel = player.channel
		room = player.room
		
		if codePartie == room.lastCodePartie and player.hasCheese:
			timeTaken = (self.server.getTime() - (player.playerStartTimeMillis if room.autoRespawn else room.gameStartTimeMillis)) * 100

			canGo = room.rooms.checkIfShamanCanGoIn(room) if player.isShaman else True
			if not canGo:
				self.sendSaveRemainingMiceMessage(channel)
				return

			player.hasCheese = False
			player.isDead = True
			player.hasEnter = True
			room.playersInPlace += 1

			place = room.playersInPlace

			player.currentPlace = place

			if room.isTutorial:
				self.sendPacket(channel, [5, 90], ByteArray().writeByte(2).toByteArray())
				t = threading.Timer(10, self.enterRoom, args=[player, self.server.rooms.getRecommendRoom(self.server.langues.getLangue(player.langueID))])
				channel.reactors.append(t)
				t.start()
				room.rooms.changeMapTime(room, 10)
			elif room.isEditeur:
				if not room.EMapValidated and room.EMapCode != 0:
					room.EMapValidated = True
					self.sendOldPacket(channel, [14, 17], [""])
			elif player.isShaman:
				pass
			else:
				room.holesType[holeType] += 1
				
				if not player.isAfk and self.server.rooms.getPlayersCountIP(room) >= int(self.server.config["needToFirst"]):
					self.skills.earnExp(player, 20)
					
					if room.isBootcamp:
						player.bootcampCount += 1
						self.sendGiveCurrency(channel, 0, 1)
						self.checkBootcampTitleUnlocked(player)
					elif room.isDefilante:
						player.cheeseCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 1
						player.seasonCheeseCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 0
						self.sendGiveCurrency(channel, 0, 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 1)
						self.checkCheeseTitleUnlocked(player)
					else:
						player.firstCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 0
						player.cheeseCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 1
						player.seasonFirstCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 0
						player.seasonCheeseCount += 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 0
						self.sendGiveCurrency(channel, 0, 3 if place == 1 else 2 if place == 2 else 1 if place == 1 else 1)
						self.checkFirstTitleUnlocked(player)
						self.checkCheeseTitleUnlocked(player)

					if not player.room.noRecords:
						sett = True

						if player.room.currentMap in player.room.rooms.records:
							record = player.room.rooms.records[player.room.currentMap]
							if (timeTaken / 100) >= record["Time"]:
								sett = False
	
						if sett:
							if not 551.1 in player.titlesList and not player.missions[51][4]:
								self.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", ["32"])
								self.skills.earnExp(player, 32)
								player.missions[51][4] = True
								player.titlesList.append(551.1)
								player.titleID = 551.1
								self.sendUnlockedTitle(player)
								self.sendTitleList(player)
								self.sendChangeTitle(player)
								self.inventory.sendNewConsumable(player, 0, 10)
								self.inventory.sendNewConsumable(player, 2, 10)
								self.inventory.sendNewConsumable(player, 3, 10)
							elif not 505.1 in player.titlesList:
								player.titlesList.append(505.1)
								player.titleID = 505.1
								self.sendUnlockedTitle(player)
								self.sendTitleList(player)
								self.sendChangeTitle(player)

							player.room.rooms.records[player.room.currentMap] = {"mapID": player.room.currentMap, "playerName": self.parsePlayerName(player), "Time": timeTaken / 100}

							self.sendLangueMessageToRoom(player.room, "", "$MessageRecord2", [self.parsePlayerName(player), str(timeTaken / 100)[:5]])

					if 1 in player.missions:
						player.missions[1][1] += 1

						if player.missions[1][1] >= player.missions[1][2]:
							if not player.missions[1][4]:
								self.sendLangueMessage(channel, player.langue.lower(), "$Mission_Complete", ["32"])
								self.skills.earnExp(player, 32)
								player.missions[1][4] = True
								self.inventory.sendNewConsumable(player, 0, 10)
								self.inventory.sendNewConsumable(player, 2, 10)
								self.inventory.sendNewConsumable(player, 3, 10)
								
				if self.server.rooms.getPlayersCount(room) >= 2:
					player.playerScore += 16 if place == 1 else 14 if place == 2 else 12 if place == 1 else 10

			room.rooms.sendAll(room, [8, 6], ByteArray().writeByte(1 if room.isDefilante else 0).writeInt(player.playerCode).writeShort(player.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
			
			if not room.isTutorial:
				if room.autoRespawn:
					self.respawnMouse(player)
				else:
					noDead = room.rooms.getPlayersNoDead(room)
					if noDead == 0:
						room.startMap()
					else:
						if (room.roundTime + room.addTime + 3 if room.count3Seconds else 0) - timeTaken / 100 > 10:
							room.rooms.changeMapTime(room, 10) 

	def sendPlayerEmote(self, player, room, emoteID, flag, others, lua):
		p = ByteArray().writeInt(player.playerCode).writeByte(emoteID)
		if not flag == "": p.writeUTF(flag)
		result = p.writeBoolean(lua).toByteArray()
		room.rooms.sendAllOthers(player, room, [8, 1], result) if others else room.rooms.sendAll(room, [8, 1], result)

	def sendShamanType(self, player, mode, canDivine):
		self.sendPacket(player.channel, [28, 10], ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(player.shamanColor, 16)).toByteArray())

	def sendAddTextArea(self, channel, id, text, posX, posY, width, height, backgroundColor, borderColor, opacity):
		self.sendPacket(channel, [29, 20], ByteArray().writeInt(id).writeUTF(text).writeShort(posX).writeShort(posY).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(opacity).writeByte(0).toByteArray())

	def sendRemoveTextArea(self, channel, id):
		self.sendPacket(channel, [29, 22], ByteArray().writeInt(id).toByteArray())

	def sendSeasonRanking(self, channel):
		self.sendAddTextArea(channel, 1, "<br><p align='center'><font size='20'><font color='#9999ff'>TEMPORADA {}</font></font></center>".format(self.server.config["season"]), 100, 60, 600, 315, int("324650", 16), int("7c97a3", 16), 100)
		self.sendAddTextArea(channel, 2, "<R><a href='event:closeSeasonMessage'><B>X</B></a></R>", 685, 60, 60, 100, 0, 0, 100)
		self.sendAddTextArea(channel, 3, "<p align='center'><font size='10'><N><B>QUEIJOS EM PRIMEIRO</B></N></font></center>", 80, 115, 225, 35, 0, 0, 100)
		self.sendAddTextArea(channel, 4, "<p align='center'><font size='10'><N><B>QUEIJOS COLETADOS</B></N></font></center>", 288, 115, 225, 35, 0, 0, 100)
		self.sendAddTextArea(channel, 5, "<p align='center'><font size='10'><N><B>RATOS SALVOS</B></N></font></center>", 488, 115, 225, 35, 0, 0, 100)

		# ranking
		rank = 0
		for playerName in self.season_ranking["first"]:
			self.sendAddTextArea(channel, 10+rank, "<p align='center'><font size='10'><N>{}. {}</N></font></center>".format(rank+1, playerName), 80, 135 + (18 * rank), 225, 35, 0, 0, 100)
			rank += 1

		# ranking
		rank = 0
		for playerName in self.season_ranking["cheese"]:
			self.sendAddTextArea(channel, 20+rank, "<p align='center'><font size='10'><N>{}. {}</N></font></center>".format(rank+1, playerName), 288, 135 + (18 * rank), 225, 35, 0, 0, 100)
			rank += 1

		# ranking
		rank = 0
		for playerName in self.season_ranking["saves"]:
			self.sendAddTextArea(channel, 30+rank, "<p align='center'><font size='10'><N>{}. {}</N></font></center>".format(rank+1, playerName), 488, 135 + (18 * rank), 225, 35, 0, 0, 100)
			rank += 1

		self.sendAddTextArea(channel, 40, "<p align='center'><font size='11'><N>Lista dos melhores jogadores desta temporada.<BR>Tente alcançar o topo da lista antes que a temporada acabe!</N></font></center>", 60, 335, 685, 100, 0, 0, 100)

		self.sendRemoveTextArea(channel, 200)

	def updateSeasonRanking(self):
		self.season_ranking = {"first": [], "cheese": [], "saves": []}

		pool = self.server.database.execute("SELECT * FROM users ORDER BY seasonFirstCount DESC LIMIT 10")
		results = self.server.database.fetchall(pool)
		for row in results:
			self.season_ranking["first"].append("{}#{}".format(row["playerName"], row["playerTag"]))

		pool = self.server.database.execute("SELECT * FROM users ORDER BY seasonCheeseCount DESC LIMIT 10")
		results = self.server.database.fetchall(pool)
		for row in results:
			self.season_ranking["cheese"].append("{}#{}".format(row["playerName"], row["playerTag"]))

		pool = self.server.database.execute("SELECT * FROM users ORDER BY seasonSavesCount DESC LIMIT 10")
		results = self.server.database.fetchall(pool)
		for row in results:
			self.season_ranking["saves"].append("{}#{}".format(row["playerName"], row["playerTag"]))

		threading.Timer(3600, self.updateSeasonRanking).start()

	def removeNoConnectedAccounts(self):
		for player in self.players.values():
			if self.server.getTime() - player.channel.lastDummyTime >= 120 or player.isLogged and self.server.getTime() - player.channel.lastPingTime >= 120:
				player.channel.close_connection()
		threading.Timer(120, self.removeNoConnectedAccounts).start()

	def sendModerationMessage(self, priv, chatID, langue, message, inTab=False):
		for player in self.players.values():
			if player.privLevel >= priv:
				self.sendPacket(player.channel, [6, 10], ByteArray().writeByte(chatID).writeUTF(langue).writeUTF(message).writeBoolean(inTab).writeBoolean(False).writeByte(0).toByteArray())