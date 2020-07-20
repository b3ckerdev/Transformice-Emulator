from server.helpers.String import *

class RCommands:
	C, CC = 6, 26

	@staticmethod
	def parse(users, channel, packet, packetID):
		command = String.filtreChatString(packet.readUTF())

		users.commands.parse(channel, command)