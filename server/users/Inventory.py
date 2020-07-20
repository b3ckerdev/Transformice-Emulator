from network.packet.ByteArray import *

class Inventory:
	def __init__(self, users):
		self.users = users
		self.server = users.server

	def equipConsumable(self, player, consumable):
		if consumable in list(player.playerConsumables):
			if consumable in player.equipedConsumables:
				player.equipedConsumables.remove(consumable)
			else:
				player.equipedConsumables.append(consumable)

	def useConsumable(self, player, consumable):
		if consumable in list(player.playerConsumables):
			player.playerConsumables[consumable] -= 1
			if player.playerConsumables[consumable] < 1:
				del player.playerConsumables[consumable]
				self.updateInventory(player, consumable, 0)
			else:
				self.updateInventory(player, consumable, player.playerConsumables[consumable])
				
			packet = ByteArray()
			packet.writeInt(player.playerCode)
			packet.writeUnsignedShort(consumable)
			self.server.rooms.sendAll(player.room, [31, 3], packet.toByteArray())

	def updateInventory(self, player, consumable, count):
		packet = ByteArray()
		packet.writeUnsignedShort(consumable)
		packet.writeUnsignedByte(250 if count > 250 else count)
		self.users.sendPacket(player.channel, [31, 2], packet.toByteArray())

	def openInventory(self, player):
		packet = ByteArray()
		packet.writeShort(len(list(player.playerConsumables)))
		for id, count in player.playerConsumables.items():
			packet.writeShort(id)
			packet.writeUnsignedByte(250 if count > 250 else count)
			packet.writeUnsignedByte(0)
			packet.writeBoolean(True)
			packet.writeBoolean(True)
			packet.writeBoolean(True)
			packet.writeBoolean(True)
			packet.writeBoolean(True)
			packet.writeBoolean(False)
			packet.writeBoolean(False)
			packet.writeUnsignedByte(player.equipedConsumables.index(id) + 1 if id in player.equipedConsumables else 0)
		self.users.sendPacket(player.channel, [31, 1], packet.toByteArray())

	def sendNewConsumable(self, player, consumable, count):
		player.playerConsumables[consumable] = count
		packet = ByteArray()
		packet.writeByte(0)
		packet.writeUnsignedShort(consumable)
		packet.writeUnsignedShort(count)
		self.users.sendPacket(player.channel, [100, 67], packet.toByteArray())