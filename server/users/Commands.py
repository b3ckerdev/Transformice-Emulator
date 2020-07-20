import time
from network.packet.ByteArray import *

class Commands:
	def __init__(self, users, rooms):
		self.users = users
		self.rooms = rooms

	def parse(self, channel, command):
		player = channel.player
		room = player.room

		arguments = command.split(" ")
		command = arguments[0].lower()
		arguments = arguments[1:]

		if command in ["codecadeau"]:
			if len(arguments) == 1:
				code = arguments[0]

				if self.users.parsePlayerName(player) in self.users.server.cache.discordCodes:
					if code != self.users.server.cache.discordCodes[self.users.parsePlayerName(player)]["code"]:
						self.users.sendLangueMessage(channel, player.langue.lower(), "<R>$Invalide</R>", [])
					elif (self.users.server.getTime() - self.users.server.cache.discordCodes[self.users.parsePlayerName(player)]["time"]) > 600:
						del self.users.server.cache.discordCodes[self.users.parsePlayerName(player)]
						self.users.sendLangueMessage(channel, player.langue.lower(), "<R>$Perime</R>", [])
					else:
						self.users.server.cache.discordCodes[self.users.parsePlayerName(player)]["completed"] = True
						self.users.sendLangueMessage(channel, player.langue.lower(), "$CertificationOK", [])
			return

		elif command in ["ping"]:
			if len(arguments) == 1:
				if player.privLevel >= 5:
					playerName = arguments[0].capitalize()
					if playerName in self.users.players:
						player2 = self.users.players[playerName]
						if player2.channel.geoIP.matched:
							msg = "<N>Connection information [{}]:</N>\n\n<BL>Ping :</BL> <V>{}ms</V>\n<BL>Connection status :</BL> <V>{}</V>\n\n<N>GeoIP [{}]:</N>\n\n<BL>Country:</BL> <V>{}</V>\n<BL>Country name :</BL> <V>{}</V>\n<BL>Region name :</BL> <V>{}</V>\n<BL>City :</BL> <V>{}</V>\n<BL>Zip code :</BL> <V>{}</V>\n<BL>Time zone :</BL> <V>{}</V>\n<BL>Latitude :</BL> <V>{}</V>\n<BL>Longitude :</BL> <V>{}</V>".format(playerName, player2.playerPing[1], "Great" if player2.playerPing[1] < 120 else "Good" if player2.playerPing[1] < 220 else "Bad" if player2.playerPing[1] < 400 else "Horrible", player2.channel.ipAddress, player2.channel.geoIP.json["country_code"], player2.channel.geoIP.json["country_name"], player2.channel.geoIP.json["region_name"], player2.channel.geoIP.json["city"], player2.channel.geoIP.json["zip_code"], player2.channel.geoIP.json["time_zone"], player2.channel.geoIP.json["latitude"], player2.channel.geoIP.json["longitude"])
							self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
						else:
							msg = "<N>Connection information [{}]:</N>\n\n<BL>Ping :</BL> <V>{}ms</V>".format(playerName, player2.playerPing[1])
							self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
					else:
						self.users.sendMessage(channel, "The player {} is not connected.".format(playerName))
			else:
				self.users.sendMessage(channel, str(player.playerPing[1]))
			return

		elif command in ["facebook"]:
			self.users.sendOldPacket(channel, [26, 19], [])

		elif command in ["vanilla"]:
			self.users.enterRoom(player, "vanilla1")
			return

		elif command in ["survivor"]:
			self.users.enterRoom(player, "survivor1")
			return

		elif command in ["racing"]:
			self.users.enterRoom(player, "racing1")
			return

		elif command in ["music"]:
			self.users.enterRoom(player, "music1")
			return

		elif command in ["bootcamp"]:
			self.users.enterRoom(player, "bootcamp1")
			return

		elif command in ["music"]:
			self.users.enterRoom(player, "music")
			return

		elif command in ["defilante"]:
			self.users.enterRoom(player, "defilante1")
			return

		elif command in ["village"]:
			self.users.enterRoom(player, "village1")
			return

		elif command in ["tutorial"]:
			self.users.enterRoom(player, "\x03[Tutorial] {}".format(self.users.parsePlayerName(player)))
			return

		elif command in ["editeur"]:
			self.users.enterRoom(player, "\x03[Editeur] {}".format(self.users.parsePlayerName(player)))
			self.users.sendOldPacket(channel, [14, 14], [])
			return

		elif command in ["pw"]:
			if self.users.parsePlayerName(player) in player.room.roomName:
				if len(arguments) == 0:
					player.room.roomPassword = ""
					self.users.sendLangueMessage(channel, player.langue.lower(), "$MDP_Desactive", [])
				else:
					player.room.roomPassword = arguments[0]
					self.users.sendLangueMessage(channel, player.langue.lower(), "$Mot_De_Passe : {}".format(player.room.roomPassword), [])
			return
			
		elif command in ["totem"]:
			if player.shamanSaves >= 0:
				#self.users.enterRoom(player, "\x03[Totem] {}".format(self.users.parsePlayerName(player)))
				self.users.sendMessage(channel, "Em desenvolvimento!")
				return

		elif command in ["pos"]:
			self.users.sendMessage(channel, "X: {}, Y: {}".format(int(player.posX), int(player.posY)))
			return

		elif command in ["mjj"]:
			if arguments[0] == "":
				roomName = "1"
			else:
				roomName = arguments[0]
			roomName = {9: "racing", 1: "", 10: "defilante", 2: "bootcamp", 8: "survivor", 3: "vanilla", 11: "music", 16: "village", 18: "*#quarentine"}[player.roomsListMode] + roomName
			self.users.enterRoom(player, roomName)
			return

		elif command in ["kill", "suicide", "mort", "die"]:
			if player.isDead:
				return
				
			self.users.sendPlayerDied(player)
			return

		elif command in ["time", "temps"]:
			t = int(player.playingTime + (self.users.server.getTime() - player.connectedTime)) * 1000
			s = str(int(t / 1000 % 60))
			m = str(int(t / (60 * 1000) % 60))
			h = str(int(t / (60 * 60 * 1000) % 24))
			d = str(int(t / (24 * 60 * 60 * 1000)))
			self.users.sendPacket(channel, [28, 5], ByteArray().writeUTF("").writeUTF("$TempsDeJeu").writeByte(4).writeUTF(d).writeUTF(h).writeUTF(m).writeUTF(s).toByteArray())

		elif command in ["title", "titulo", "titre"]:
			if len(arguments) == 0:
				p = ByteArray().writeShort(len(player.titlesList))
				for title in player.titlesList:
					p.writeShort(int(title))
				self.users.sendPacket(channel, [8, 14], p.writeShort(0).toByteArray()) 
			elif len(arguments) == 1 and arguments[0].isdigit():
				for title in player.titlesList:
					if int(title) == int(arguments[0]):
						player.titleID = title
						self.users.sendPacket(channel, [100, 72], ByteArray().writeUnsignedByte(player.gender).writeShort(int(title)).toByteArray())
			else:
				pass
			return

		elif command in ["profil", "perfil", "profile"]:
			playerName = self.users.parsePlayerName(player) if len(arguments) == 0 else arguments[0].capitalize()
			if playerName in self.users.players:
				self.users.sendProfile(player, playerName) 
			return

		elif command in ["ref", "referral", "referrals", "parrain"]:
			if len(arguments) == 1:
				if player.privLevel >= 5:
					playerName = arguments[0].capitalize()
					if playerName in self.users.players:
						player2 = self.users.players[playerName]
						msg = "<N>Referrals [{}]:</N>\n\n<BL>Total referrals :</BL> <V>{}</V>".format(playerName, player2.referrals)
						self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
					else:
						self.users.sendMessage(channel, "The player {} is not connected.".format(playerName))
			else:
				self.users.sendMessage(channel, "Referrals: {}\nYour referral link: {}/?ref={}".format(player.referrals, self.users.server.config["url"], player.playerID))
			return

		elif command in ["info"]:
			if room.currentMap in self.rooms.records:
				record = self.rooms.records[room.currentMap]
				self.users.sendMessage(channel, "{} - @{} - P{} - {} - {}s".format(room.currentName, room.currentMap, room.currentPerm, str(record["Time"])[:5], record["playerName"]))
			else:
				self.users.sendMessage(channel, "{} - @{} - P{}".format(room.currentName, room.currentMap, room.currentPerm))
			return

		elif command in ["myrecords", "myrecord"]:
			msg = ["<N>Record's list:</N>\n"]
			c = 0
			for record in self.rooms.records.values():
				if record["playerName"] == self.users.parsePlayerName(player):
					c += 1
					msg.append("<BL>@{} - {}s</BL>".format(record["mapID"], str(record["Time"])[:5]))
			msg.append("\n<J>Total:</J> <R>{}</R>".format(c))
			msg = "\n".join(msg)
			self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		elif command in ["mod"]:
			players_c = {}
			for player2 in self.users.players.values():
				if player2.privLevel > 4 and player2.privLevel < 10 and player2.privLevel != 7 and not player2.isHide:
					if not player2.langue in players_c:
						players_c[player2.langue] = []
					players_c[player2.langue].append("<BV>{}</BV>".format(self.users.parsePlayerName(player2)))
			msg = []
			for comm, players in players_c.items():
				msg.append("<BL>[{}]</BL> {}".format(comm.lower(), ", ".join(players)))
			self.users.sendPacket(channel, [28, 5], ByteArray().writeUTF("").writeUTF("$ModoEnLigne \n{}".format("\n".join(msg)) if len(msg) > 0 else "$ModoPasEnLigne").writeByte(0).toByteArray())
			return

		elif command in ["mapcrew"]:
			players_c = {}
			for player2 in self.users.players.values():
				if player2.isMapcrew and player2.privLevel < 10 and not player2.isHide:
					if not player2.langue in players_c:
						players_c[player2.langue] = []
					players_c[player2.langue].append("<BV>{}</BV>".format(self.users.parsePlayerName(player2)))
			msg = []
			for comm, players in players_c.items():
				msg.append("<BL>[{}]</BL> {}".format(comm.lower(), ", ".join(players)))
			self.users.sendPacket(channel, [28, 5], ByteArray().writeUTF("").writeUTF("$MapcrewEnLigne \n{}".format("\n".join(msg)) if len(msg) > 0 else "$MapcrewPasEnLigne").writeByte(0).toByteArray())
			return

		elif command in ["help"]:
			msg = ["<J>(!)</J> <N>Você pode rolar esta lista usando a roda do mouse ou o controle deslizante à direita.</N>\n"]
			msg.append("<VP>Lista de comandos disponíveis:</VP>")
			msg.append("<N>/info - Exibir informações do mapa atual.</N>")
			msg.append("<N>/pos - Coordenadas do rato.</N>")
			msg.append("<N>/ping - Exibir seu ping.</N>")
			msg.append("<N>/referral - Exibir seu link de referência.</N>")
			msg.append("<N>/mod - Mostrar lista de moderadores online.</N>")
			msg.append("<N>/mapcrew - Mostrar lista de Map Crew online.</N>")
			msg.append("<N>/time - Exibir o tempo de jogo da sua conta.</N>")
			msg.append("<N>/staff - Exibir lista de membros da moderação.</N>")
			msg.append("<N>/myrecords - Exibir lista de recordes batidos por você.</N>")
			if player.isVip or player.privLevel >= 3:
				msg.append("<N>/vip - Exibir lista de membros VIP.</N>")
				msg.append("<N>/colornick #ffffff - Alterar a cor do seu apelido.</N>")
				msg.append("<N>/colormouse #ffffff - Alterar a cor do seu rato.</N>")
			msg = "\n".join(msg)
			self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		# staff
		elif command in ["staff"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				msg = ["<N>Staff list: </N>\n"]
				pool = self.users.server.database.execute("SELECT * FROM users WHERE Privilege > 2 ORDER BY Privilege DESC")
				results = self.users.server.database.fetchall(pool)
				for row in results:
					ranks = {3: "Arbitre", 5: "Moderator", 7: "Moderator Secret", 8: "Community Manager", 9: "CO-Admin", 10: "Admin"}
					rank = "Undefined"
					if row["Privilege"] in list(ranks):
						rank = ranks[row["Privilege"]]
					msg.append("<BL>{}#{}</BL> : <V>{}</V>".format(row["playerName"], row["playerTag"], rank))
				msg = "\n".join(msg)
				self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		elif command in ["ls"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				startswit = " ".join(arguments)
				msg = ["<N>List of rooms:</N>\n"] if len(startswit) == 0 else ["<N>List of rooms matching [{}]</N>\n".format(startswit)]
				players = 0
				for roomName, room in self.rooms.rooms.items():
					if startswit in roomName:
						players += self.rooms.getPlayersCount(room)
						msg.append("<BL>{} :</BL> <b><V>{}</V></b>".format(roomName, self.rooms.getPlayersCount(room)))
				msg.append("\n<J>Total players:</J> <R>{}</R>".format(players))
				msg = "\n".join(msg)
				self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		elif command in ["lsplayers"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				startswit = " ".join(arguments)
				msg = ["<N>List of players:</N>\n"] if len(startswit) == 0 else ["<N>List of players matching [{}]</N>\n".format(startswit)]
				players = 0
				for roomName, room in self.rooms.rooms.items():
					if startswit in roomName:
						players += self.rooms.getPlayersCount(room)
						for player2 in room.players.values():
							msg.append("<BL>{} ({})</BL>".format(self.users.parsePlayerName(player2), roomName))
				msg.append("\n<J>Total players:</J> <R>{}</R>".format(players))
				msg = "\n".join(msg)
				self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		elif command in ["join"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) != 1:
					return
				playerName = arguments[0].capitalize()

				if playerName == self.users.parsePlayerName(player):
					self.users.sendMessage(channel, "You cannot use this command on yourself.")
				elif playerName in self.users.players:
					roomName = self.users.players[playerName].room.roomName
					roomName = roomName if "*" == roomName[:1] else roomName[3:]
					self.users.enterRoom(player, roomName)
				else:
					self.users.sendMessage(channel, "The player {} is not connected.".format(playerName))
			return

		elif command in ["find"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) != 1:
					return
				playerName = arguments[0].capitalize()

				if playerName == self.users.parsePlayerName(player):
					self.users.sendMessage(channel, "You cannot use this command on yourself.")
				elif playerName in self.users.players:
					roomName = self.users.players[playerName].room.roomName
					self.users.sendMessage(channel, "[<V>{}</V>] -> <V>{}</V>".format(playerName, roomName))
				else:
					self.users.sendMessage(channel, "The player {} is not connected.".format(playerName))
			return

		elif command in ["loginlog"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) != 1:
					return
				isIP = False
				if "." in playerName:
					isIP = True
				if isIP:
					msg = ["<N>Login list by IP: <V>{}</V></N>\n".format(arguments[0])] 
					pool = self.users.server.database.execute("SELECT * FROM loginlog WHERE ip = %s", (arguments[0],))
					results = self.users.server.database.fetchall(pool)
					for result in results:
						msg.append("<BL>{} ({}) :</BL> <b><V>{}</V></b>".format(result["ip"], result["date"], result["playerName"]))
					msg = "\n".join(msg)
					self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
				else:
					playerName = arguments[0].capitalize()
					msg = ["<N>Login list by: <V>{}</V></N>\n".format(playerName)] 
					pool = self.users.server.database.execute("SELECT * FROM loginlog WHERE playerName = %s", (playerName,))
					results = self.users.server.database.fetchall(pool)
					for result in results:
						msg.append("<BL>{} ({}) :</BL> <b><V>{}</V></b>".format(result["playerName"], result["date"], result["ip"]))
					msg = "\n".join(msg)
					self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		# admin
		elif command in ["moveall"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) > 0:
					oldRoomName = player.room.roomName
					roomName = " ".join(arguments)

					p = list(player.room.players.values())

					for player2 in p:
						self.users.enterRoom(player2, roomName)

					self.users.sendMessageToPriv(5, "{} moved all players from room {} to room {}.".format(self.users.parsePlayerName(player), oldRoomName, player.room.roomName), False)
			return

		elif command in ["np"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1 and arguments[0][:1] == "@" and arguments[0][1:].isdigit():
					pool = self.users.server.database.execute("SELECT * FROM maps WHERE mapID = %s", (int(arguments[0][1:]),))
					results = self.users.server.database.fetchone(pool)
					if results != None:
						player.room.nextMapID = int(arguments[0][1:])
						player.room.startMap()
					else:
						self.users.sendLangueMessage(channel, player.langue.lower(), "$CarteIntrouvable", [])
				else:
					player.room.startMap()
			return

		elif command in ["npp"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1 and arguments[0][:1] == "@" and arguments[0][1:].isdigit():
					pool = self.users.server.database.execute("SELECT * FROM maps WHERE mapID = %s", (int(arguments[0][1:]),))
					results = self.users.server.database.fetchone(pool)
					if results != None:
						player.room.nextMapID = int(arguments[0][1:])
						self.users.sendLangueMessage(channel, player.langue.lower(), "$ProchaineCarteAvecInfo", [arguments[0]])
					else:
						self.users.sendLangueMessage(channel, player.langue.lower(), "$CarteIntrouvable", [])
			return

		elif command in ["levetest"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				player.room.leveTest = True
				for player2 in player.room.players.values():
					if player2.privLevel >= 5:
						self.users.sendMessage2(player2.channel, "<VP>LEVE TEST IN NEXT MAP!</VP>")
			return

		elif command in ["tfmapi"]:
			if player.privLevel >= 5 and len(arguments) == 1 and arguments[0][:1] == "@" and arguments[0][1:].isdigit():
				code = int(arguments[0][1:])
				if not code in self.users.server.api.mapsAwait:
					self.users.server.api.mapsAwait.append(code)
			return

		elif command in ["priv"]:
			if player.privLevel >= 10 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 2 and arguments[1].isdigit() and int(arguments[1]) > 0 and int(arguments[1]) < 11:
					playerName = arguments[0].capitalize()
					priv = int(arguments[1])

					if priv < 1:
						priv = 1
					if priv > 10:
						priv = 10

					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						self.users.players[playerName].privLevel = priv
						self.users.sendMessage(channel, "Done.")
					elif self.users.checkPlayerNameExist(playerName):
						pool = self.users.server.database.execute("UPDATE users SET Privilege = %s WHERE playerName = %s AND playerTag = %s", (priv, playerName.split("#")[0], playerName.split("#")[1]))
						self.users.server.database.commitAll()
						self.users.sendMessage(channel, "Done.")
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		# vip
		elif command in ["vip", "vips"]:
			if player.isVip or player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				msg = ["<p align='center'><N>VIP's list: </N>\n"]
				pool = self.users.server.database.execute("SELECT * FROM users WHERE isVip = 1")
				resultss = self.users.server.database.fetchall(pool)
				for row in resultss:
					if row["isVip"] == 1:
						msg.append("<BL>{}#{}</BL>".format(row["playerName"], row["playerTag"]))
				msg.append("</p>")
				msg = "\n".join(msg)
				self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			else:
				self.users.sendLangueMessage(channel, player.langue.lower(), "$erreur.tribulle.17", [])
			return

		elif command in ["re"]:
			if player.isVip or player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if player.isDead:
					self.users.respawnSpecific(player)
			return

		elif command in ["colornick"]:
			if player.isVip or player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 2:
					color = arguments[1]
					if color.isdigit():
						color = "%06X" %(0xffffff & int(color))
						player.colorNick = color
						self.users.sendMessage2(channel, "<J>Done.</J>")
			else:
				self.users.sendLangueMessage(channel, player.langue.lower(), "$erreur.tribulle.17", [])
			return

		elif command in ["colormouse"]:
			if player.isVip or player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 2:
					color = arguments[1]
					if color.isdigit():
						color = "%06X" %(0xffffff & int(color))
						player.mouseColor = color
						self.users.sendMessage2(channel, "<J>Done.</J>")
			else:
				self.users.sendLangueMessage(channel, player.langue.lower(), "$erreur.tribulle.17", [])
			return

		# funcorp
		elif command in ["funcorp"]:
			if player.isFuncorp:
				if len(arguments) == 0:
					if player.room.isFuncorp:
						for player2 in player.room.players.values():
							player2.funColor = ""
							player2.funMouseColor = ""
						player.room.isFuncorp = False
						player.room.kickeds = []
						player.room.rooms.sendLangueMessageToRoom(player.room, player.langue.lower(), "<CEP>$FunCorpDesactive</CEP>", [])
						for player2 in self.users.players.values():
							if player2.isFuncorp:
								self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Funcorp finished in room {}.".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
					else:
						player.room.isFuncorp = True
						player.room.rooms.sendLangueMessageToRoom(player.room, player.langue.lower(), "<CEP>$FunCorpActive</CEP>", [])
						for player2 in self.users.players.values():
							if player2.isFuncorp:
								self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Funcorp started in room {}.".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
					return

				elif len(arguments) == 1 and player.room.isFuncorp:
					comm = arguments[0].lower()

					if comm in ["public"]:
						if player.room.isPublic:
							player.room.isPublic = False
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The {} room is now private.".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
						else:
							player.room.isPublic = True
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The {} room is now public.".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
					return

				elif len(arguments) == 2 and player.room.isFuncorp:
					comm = arguments[0].lower()
					playerName = arguments[1].capitalize()

					if playerName.lower() != "all":
						if not playerName in list(player.room.players):
							self.users.sendLangueMessage(player.channel, player.langue.lower(), "$chat.message.joueurInexistant", [playerName])
							return

					if comm in ["kick"]:
						if playerName.lower() != "all":
							player.room.kickeds.append(playerName)
							player2 = player.room.players[playerName]
							self.users.sendLangueMessage(player2.channel, player.langue.lower(), "<R>$TournoiPerdu</R>", [])
							player2.room.rooms.getRecommendRoom(self.users.server.langues.getLangue(player2.langueID))
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("{} was kicked out of the room.".format(playerName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
						return

					elif comm in ["glider"]: #traduzir
						if playerName.lower() == "all":
							for player2 in player.room.players.values():
								player.room.rooms.sendAll(player.room, [5, 33], ByteArray().writeByte(1).writeInt(player2.playerCode).toByteArray())
								
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Glider skill activated in room {} (all).".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())

						else:
							player2 = player.room.players[playerName]
							player.room.rooms.sendAll(player.room, [5, 33], ByteArray().writeByte(1).writeInt(player2.playerCode).toByteArray())
							
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Glider skill activated in room {} ({}).".format(player.room.roomName, playerName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())

					elif comm in ["rotate"]: #traduzir
						if playerName.lower() == "all":
							for player2 in player.room.players.values():
								player.room.rooms.sendAll(player.room, [5, 30], ByteArray().writeInt(player2.playerCode).toByteArray())
								
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Ability to rotate activated in room {} (all).".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())

						else:
							player2 = player.room.players[playerName]
							player.room.rooms.sendAll(player.room, [5, 30], ByteArray().writeInt(player2.playerCode).toByteArray())
							
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Ability to rotate activated in room {} ({}).".format(player.room.roomName, playerName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())

					elif comm in ["transformation"]: #traduzir
						if playerName.lower() == "all":
							for player2 in player.room.players.values():
								self.users.sendTransformation(player2.channel, True)
	
							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Transformation skill activated in room {} (all).".format(player.room.roomName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())

						else:
							player2 = player.room.players[playerName]
							self.users.sendTransformation(player2.channel, True)

							for player2 in self.users.players.values():
								if player2.isFuncorp:
									self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("Transformation skill activated in room {} ({}).".format(player.room.roomName, playerName)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
					return

				elif len(arguments) == 3 and player.room.isFuncorp:
					comm = arguments[0].lower()
					playerName = arguments[1].capitalize()
					value = arguments[2]

					if playerName.lower() != "all":
						if not playerName in list(player.room.players):
							self.users.sendLangueMessage(player.channel, player.langue.lower(), "$chat.message.joueurInexistant", [playerName])
							return

					if comm in ["colornick"]:
						if len(value) == 7 and value[:1] == "#":
							if playerName.lower() == "all":
								for player2 in player.room.players.values():
									player2.funColor = value.lower()[1:].lower()
								
								for player2 in self.users.players.values():
									if player2.isFuncorp:
										self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The nickname color changed in room {} ({}).".format(player.room.roomName, value)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
							else:
								player2 = player.room.players[playerName]
								player2.funColor = value.lower()[1:].lower()
								for player2 in self.users.players.values():
									if player2.isFuncorp:
										self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The color of the nickname for {} changed in room {} ({}).".format(playerName, player.room.roomName, value)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
						return

					elif comm in ["colormouse"]:
						if len(value) == 7 and value[:1] == "#":
							if playerName.lower() == "all":
								for player2 in player.room.players.values():
									player2.funMouseColor = value.lower()[1:].lower()

								for player2 in self.users.players.values():
									if player2.isFuncorp:
										self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The color of the mice changed in room {} ({}).".format(player.room.roomName, value)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
							else:
								player2 = player.room.players[playerName]
								player2.funMouseColor = value.lower()[1:].lower()
								for player2 in self.users.players.values():
									if player2.isFuncorp:
										self.users.sendPacket(player2.channel, [6, 10], ByteArray().writeByte(9).writeUTF(self.users.parsePlayerName(player)).writeUTF("The color of the {} mouse changed in room {} ({}).".format(playerName, player.room.roomName, value)).writeBoolean(False).writeBoolean(False).writeByte(0).toByteArray())
						return

					return
			return

		# staff
		elif command in ["hide"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if not player.isHide:
					player.isHide = True
					player.isDead = True
					self.users.sendPlayerDisconnect(player.room, player)
					self.users.sendMessage(channel, "You are invisible.")
			return

		elif command in ["unhide"]:
			if player.privLevel >= 3 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if player.isHide:
					player.isHide = False
					self.rooms.sendAll(player.room, [144, 2], ByteArray().writeBytes(self.rooms.server.users.getPlayerData(player)).writeBoolean(False).writeBoolean(True).toByteArray())
					self.users.sendMessage(channel, "You are visible.")
			return
			
		elif command in ["mute", "imute"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) < 3:
					return

				if not arguments[1].isdigit():
					return

				playerName = arguments[0].capitalize()
				hours = int(arguments[1])
				if hours < 1:
					hours = 1
				elif hours > 360:
					hours = 360
				else:
					hours = hours
				reason = " ".join(arguments[2:])
				imute = command == "imute"

				if reason == "":
					return

				if playerName in self.users.server.config["privileged"]:
					return
				elif playerName == self.users.parsePlayerName(player):
					self.users.sendMessage(channel, "You cannot use this command on yourself.")
				elif playerName in self.users.players:
					h = self.users.server.getTime() + (hours * 60 * 60)

					player2 = self.users.players[playerName]

					self.users.server.mutes[playerName] = {"time": h, "reason": reason, "by": self.users.parsePlayerName(player)}

					pool = self.users.server.database.execute("INSERT INTO sanctions (type, playerName, hours, reason, by_) VALUES (%s, %s, %s, %s, %s)", (0, playerName, h, reason, self.users.parsePlayerName(player)))
					self.users.server.database.commitAll()
					
					self.users.sendMessageToPriv(3, "{} muted the player {} for {}h ({}).".format(self.users.parsePlayerName(player), playerName, hours, reason), False)

					self.users.sendLangueMessage(player2.channel, player2.langue.lower(), "<ROSE>$MuteInfo1", [str(hours), reason])
					
					if not imute:
						self.users.sendLangueMessageToRoom(player2.room, player2.langue.lower(), "<ROSE>$MuteInfo2", [playerName, str(hours), reason], player2)
				
					if playerName in self.users.server.modopwet.reports["names"]:
						self.users.server.modopwet.updateModoPwet()

				elif self.users.checkPlayerNameExist(playerName):
					h = self.users.server.getTime() + (hours * 60 * 60)
					self.users.server.mutes[playerName] = {"time": h, "reason": reason, "by": self.users.parsePlayerName(player)}

					pool = self.users.server.database.execute("INSERT INTO sanctions (type, playerName, hours, reason, by_) VALUES (%s, %s, %s, %s, %s)", (0, playerName, h, reason, self.users.parsePlayerName(player)))
					self.users.server.database.commitAll()

					self.users.sendMessageToPriv(3, "{} muted the player {} for {}h ({}).".format(self.users.parsePlayerName(player), playerName, hours, reason), False)
				else:
					self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["unmute"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) != 1:
					return
				playerName = arguments[0].capitalize()

				if playerName in self.users.server.mutes:
					del self.users.server.mutes[playerName]

					self.users.sendMessageToPriv(3, "{} removed the mute from player {}.".format(self.users.parsePlayerName(player), playerName), False)
				else:
					self.users.sendMessage(channel, "The account {} is not muted.".format(playerName))
			return

		elif command in ["ban", "iban"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) < 3:
					return

				if not arguments[1].isdigit():
					return

				playerName = arguments[0].capitalize()
				hours = int(arguments[1])
				if hours < 1:
					hours = 1
				elif hours > 360:
					hours = 360
				else:
					hours = hours
				reason = " ".join(arguments[2:])
				iban = command == "iban"

				if reason == "":
					return

				if playerName in self.users.server.config["privileged"]:
					return
				elif playerName == self.users.parsePlayerName(player):
					self.users.sendMessage(channel, "You cannot use this command on yourself.")
				elif playerName in self.users.players:
					h = self.users.server.getTime() + (hours * 60 * 60)
					
					player2 = self.users.players[playerName]

					self.users.server.ipBans[player2.channel.ipAddress] = {"time": h, "reason": reason, "by": self.users.parsePlayerName(player)}
					self.users.server.bans[playerName] = {"time": h, "reason": reason, "by": self.users.parsePlayerName(player)}

					pool = self.users.server.database.execute("INSERT INTO sanctions (type, playerName, hours, reason, by_) VALUES (%s, %s, %s, %s, %s)", (1, playerName, h, reason, self.users.parsePlayerName(player)))
					self.users.server.database.commitAll()

					self.users.sendMessageToPriv(3, "{} banned the player {} for {}h ({}).".format(self.users.parsePlayerName(player), playerName, hours, reason), False)

					if not iban:
						self.users.sendLangueMessageToRoom(player2.room, player2.langue.lower(), "<ROSE>$Message_Ban", [playerName, str(hours), reason], player2)

					for player3 in self.users.players.values():
						if player3.channel.ipAddress == player2.channel.ipAddress:
							self.users.sendOldPacket(player3.channel, [26, 18], [str(hours * 3600000), reason])
							player3.channel.close_connection()

					if playerName in self.users.server.modopwet.reports["names"]:
						self.users.server.modopwet.reports[playerName]["status"] = "banned"
						self.users.server.modopwet.reports[playerName]["banhours"] = hours
						self.users.server.modopwet.reports[playerName]["banreason"] = reason
						self.users.server.modopwet.reports[playerName]["bannedby"] = self.users.parsePlayerName(player)
						for playerName2 in self.users.server.modopwet.reports[playerName]["reporters"]:
							if playerName2 in self.users.players:
								player3 = self.users.players[playerName2]
								player3.karmas += 1
								self.users.sendLangueMessage(player3.channel, player3.langue.lower(), "$Traitement_Signalement (karma: {})".format(player3.karmas), [playerName])

						self.users.server.modopwet.updateModoPwet()

				elif self.users.checkPlayerNameExist(playerName):
					h = self.users.server.getTime() + (hours * 60 * 60)

					self.users.server.bans[playerName] = {"time": h, "reason": reason, "by": self.users.parsePlayerName(player)}

					pool = self.users.server.database.execute("INSERT INTO sanctions (type, playerName, hours, reason, by_) VALUES (%s, %s, %s, %s, %s)", (1, playerName, h, reason, self.users.parsePlayerName(player)))
					self.users.server.database.commitAll()

					self.users.sendMessageToPriv(3, "{} banned the player {} for {}h ({}).".format(self.users.parsePlayerName(player), playerName, hours, reason), False)
				else:
					self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["unban"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) != 1:
					return

				playerName = arguments[0].capitalize()

				if playerName in self.users.server.bans:
					del self.users.server.bans[playerName]

					self.users.sendMessageToPriv(3, "{} removed the ban from player {}.".format(self.users.parsePlayerName(player), playerName), False)
				else:
					self.users.sendMessage(channel, "The account {} is not banned.".format(playerName))
			return

		elif command in ["word"]:
			if player.privLevel >= 5 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 2:
					if arguments[0] == "add":
						word = arguments[1].lower()
						if len(word) < 3:
							return
						if word in self.users.server.words:
							self.users.sendMessage(channel, "This word is already in the bad words list.")
						else:
							self.users.server.words.append(word)
							self.users.sendMessageToPriv(3, "{} added the word {} to the list of bad words.".format(self.users.parsePlayerName(player), word), False)
					
					if arguments[1] == "remove":
						word = arguments[1].lower()
						if len(word) < 3:
							return
						if word in self.users.server.words:
							self.users.server.words.remove(word)
							self.users.sendMessageToPriv(3, "{} removed the word {} to the list of bad words.".format(self.users.parsePlayerName(player), word), False)
						else:
							self.users.sendMessage(channel, "This word is not in the bad words list.")
				else:
					msg = "<N>List of bad words:</V>\n\n<BL>{}</BL>".format(", ".join(self.users.server.words))
					self.users.sendPacket(channel, [28, 46], ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(msg) >> 16) & 0xFF).writeUnsignedByte((len(msg) >> 8) & 0xFF).writeUnsignedByte(len(msg) & 0xFF).writeBytes(msg.encode()).toByteArray())
			return

		elif command in ["chatlog"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()

					if playerName in list(self.users.players):
						self.users.server.modopwet.sendChatLog(player, self.users.players[playerName])
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["setvip"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()
					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						player2 = self.users.players[playerName]
						player2.isVip = True
						if not "V.I.P" in player2.chats:
							player2.chats.append("V.I.P")
							if not "V.I.P" in list(self.users.server.chats):
								self.users.server.chats["V.I.P"] = []
							self.users.server.chats["V.I.P"].append(playerName)
							self.users.server.tribulle.sendChatJoin(player2, "V.I.P")
						self.users.sendMessage(player2.channel, "<R>Parabéns, você acaba de se tornar um VIP!</R>")
						self.users.sendMessage(channel, "Done.")
					elif self.users.checkPlayerNameExist(playerName):
						pool = self.users.server.database.execute("UPDATE users SET isVip = %s WHERE playerName = %s AND playerTag = %s", (1, playerName.split("#")[0], playerName.split("#")[1]))
						self.users.server.database.commitAll()
						self.users.sendMessage(channel, "Done.")
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["delvip"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()
					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						player2 = self.users.players[playerName]
						player2.isVip = False
						if "V.I.P" in player2.chats:
							player2.chats.remove("V.I.P")
							self.users.server.chats["V.I.P"].remove(playerName)
						self.users.sendMessage(channel, "Done.")
					elif self.users.checkPlayerNameExist(playerName):
						pool = self.users.server.database.execute("UPDATE users SET isVip = %s WHERE playerName = %s AND playerTag = %s", (0, playerName.split("#")[0], playerName.split("#")[1]))
						self.users.server.database.commitAll()
						self.users.sendMessage(channel, "Done.")
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return
			
		elif command in ["setfuncorp"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()
					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						player2 = self.users.players[playerName]
						player2.isFuncorp = True
						self.users.sendMessage(channel, "Done.")
					elif self.users.checkPlayerNameExist(playerName):
						pool = self.users.server.database.execute("UPDATE users SET isFuncorp = %s WHERE playerName = %s AND playerTag = %s", (1, playerName.split("#")[0], playerName.split("#")[1]))
						self.users.server.database.commitAll()
						self.users.sendMessage(channel, "Done.")
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["delfuncorp"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()
					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						player2 = self.users.players[playerName]
						player2.isFuncorp = False
						self.users.sendMessage(channel, "Done.")
					elif self.users.checkPlayerNameExist(playerName):
						pool = self.users.server.database.execute("UPDATE users SET isFuncorp = %s WHERE playerName = %s AND playerTag = %s", (0, playerName.split("#")[0], playerName.split("#")[1]))
						self.users.server.database.commitAll()
						self.users.sendMessage(channel, "Done.")
					else:
						self.users.sendMessage(channel, "The account {} doesn't exist.".format(playerName))
			return

		elif command in ["kick"]:
			if player.privLevel >= 8 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				if len(arguments) == 1:
					playerName = arguments[0].capitalize()

					if playerName in self.users.server.config["privileged"]:
						return
					elif playerName == self.users.parsePlayerName(player):
						self.users.sendMessage(channel, "You cannot use this command on yourself.")
					elif playerName in self.users.players:
						player2 = self.users.players[playerName]
						player2.channel.close_connection()
						self.users.sendMessageToPriv(3, "{} kicked {}.".format(self.users.parsePlayerName(player), playerName), False)
					else:
						self.users.sendMessage(channel, "The account {} is not connected.".format(playerName))
			return
			
		elif command in ["kickall"]:
			if player.privLevel >= 10 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				for player2 in self.users.players.values():
					player2.channel.close_connection()
			return

		elif command in ["resetrecords"]:
			if player.privLevel >= 10 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				self.rooms.records = {}
			return

		elif command in ["newseason"]:
			if player.privLevel >= 10 or self.users.parsePlayerName(player) in self.users.server.config["privileged"]:
				self.users.server.config["season"] += 1
				self.users.server.config["season_started_date"] = self.users.server.getTime()
				self.users.sendMessageToPriv(3, "{} has started a new season!".format(self.users.parsePlayerName(player)), False)
				for player2 in player.room.players.values():
					player2.seasonFirstCount = 0
					player2.seasonCheeseCount = 0
					player2.seasonSavesCount = 0
					self.users.sendMessage2(player2.channel, "<ROSE>UMA NOVA TEMPORADA ACABA DE INICIAR ({})!</ROSE>".format(self.users.server.config["season"]))
				pool = self.users.server.database.execute("UPDATE users SET seasonFirstCount = 0 AND seasonCheeseCount = 0 AND seasonSavesCount = 0")
				self.users.server.database.commitAll()
				self.users.updateSeasonRanking()
			return