import asyncio, time
from server.player.Player import *
from server.geoip.GeoIP import *
from server.helpers.Timer import *
from network.packet.ByteArray import *
from network.packet.ParsePackets import *
from network.codecs.MessageEncoder import *
from network.codecs.MessageDecoder import *

class ClientHandler(asyncio.Protocol):
	def __init__(self, server):
		self.server = server
		self.parse = None
		self.player = None
		self.geoIP = None
		self.ipAddress = ""
		self.recvID = 0
		self.lastPacket = b""
		self.lastDummyTime = 0
		self.lastPingTime = 0
		self.errors = 0

		self.reactors = []

		self.packetID = 0

		self.isClosed = False
		self.isValidated = False
		self.isDoS = False

	def connection_made(self, transport):
		self.transport = transport
		self.ipAddress = transport.get_extra_info('peername')[0]

		n = self.server.dos.new(self.ipAddress)

		if n == 0:
			self.isDoS = True
		if n == 1 or n == 2:
			self.isDoS = True
			self.close_connection()
		else:
			self.server.clients.append(self)

			self.parse = ParsePackets(self.server.users)
			self.player = Player(self.server, self)

			self.geoIP = GeoIP(self)

			self.lastDummyTime = self.server.getTime()

	def connection_lost(self, reason=""):
		self.close_connection(reason)

	def close_connection(self, reason=""):
		if self.isClosed:
			return
			
		self.isClosed = True

		if not self.isDoS:
			for reac in self.reactors:
				reac.cancel()
				self.reactors.remove(reac)

			if self.player.isLogged:
				if self.server.users.parsePlayerName(self.player) in self.server.modopwet.reports["names"]:
					if not self.server.modopwet.reports[self.server.users.parsePlayerName(self.player)]["status"] == "banned":
						self.server.modopwet.reports[self.server.users.parsePlayerName(self.player)]["status"] = "disconnected"
						self.server.modopwet.updateModoPwet()

				for friend in self.server.tribulle.getFriendsClass(self.player):
					self.server.tribulle.sendFriendDisconnected(self.player, friend)

				for chatName in self.player.chats:
					self.server.chats[chatName].remove(self.server.users.parsePlayerName(self.player))

					if len(self.server.chats[chatName]) == 0:
						del self.server.chats[chatName]
						
				if self.player.room != None:
					self.server.rooms.leaveRoom(self.player, self.player.room.roomName)

				self.player.lastLogin = self.server.getTime()

				self.server.users.updateDatabase(self.player)

				del self.server.users.players[self.server.users.parsePlayerName(self.player)]

			self.server.clients.remove(self)

			self.server.dos.lost(self.ipAddress)

		self.transport.close()

	def writeData(self, data):
		MessageEncoder.writeRequested(self, data)

	def data_received(self, data):
		if self.isDoS or self.isClosed:
			return

		if self.server.dos.data(self.ipAddress, data):
			data = MessageDecoder.decode(self, data)
			if data != None:
				if len(self.lastPacket) > 0:
					data = self.lastPacket + data
					self.lastPacket = b""
				self.parsePacket(ByteArray(data), data)
		else:
			self.close_connection()

	def parsePacket(self, packet, buff):
		if packet.length() > 0:

			x = 0
			length = 0

			byte1 = (packet.readByte() & 0xFF)
			length = (length | ((byte1 & 127) << (x * 7)))
			x += 1
			
			while (byte1 & 128) == 128 and x < 5:
				if not packet.bytesAvailable():
					return
				byte1 = (packet.readByte() & 0xFF)
				length = (length | ((byte1 & 127) << (x * 7)))
				x += 1

			if length != 0:
				packetID = packet.readByte() 
				if packet.length() == length:
					if packet.length() >= 2:
						self.parse.parsePacket(self, packet, packetID)
				elif packet.length() < length:
					self.lastPacket = buff
				elif packet.length() > length:
					data = packet.read(length)
					if length >= 2:
						self.parse.parsePacket(self, ByteArray(data), packetID);
					if packet.length() >= 2:
						self.parsePacket(packet, packet.toByteArray())