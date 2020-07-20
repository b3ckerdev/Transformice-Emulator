from network.packet.ByteArray import *

class MouseMovement:
	C, CC = 4, 4

	@staticmethod
	def parse(users, channel, packet, packetID):
		codePartie = packet.readInt()
		droiteEnCours = packet.readBoolean()
		gaucheEnCours = packet.readBoolean()
		px = packet.readInt()
		py = packet.readInt()
		vx = packet.readUnsignedShort()
		vy = packet.readUnsignedShort()
		jump = packet.readBoolean()
		jump_img = packet.readByte()
		portal = packet.readByte()
		isAngle = packet.bytesAvailable()
		angle = packet.readUnsignedShort() if isAngle else -1
		vel_angle = packet.readUnsignedShort() if isAngle else -1
		loc1 = packet.readBoolean() if isAngle else False
		player = channel.player
		room = player.room
		if codePartie == room.lastCodePartie:
			if droiteEnCours or gaucheEnCours:
				player.isMovingRight = droiteEnCours
				player.isMovingLeft = gaucheEnCours

				if player.isAfk:
					player.isAfk = False
					player.lastAfkTime = users.server.getTime()

				player.posX = px * 800 / 2700
				player.posY = py * 800 / 2700
				player.velX = vx
				player.velY = vy
				player.isJumping = jump
		
			packet2 = ByteArray().writeInt(player.playerCode).writeInt(codePartie).writeBoolean(droiteEnCours).writeBoolean(gaucheEnCours).writeInt(px).writeInt(py).writeUnsignedShort(vx).writeUnsignedShort(vy).writeBoolean(jump).writeByte(jump_img).writeByte(portal)
			if isAngle:
				packet2.writeUnsignedShort(angle).writeUnsignedShort(vel_angle).writeBoolean(loc1) 
			users.server.rooms.sendAllOthers(channel.player, room, [4, 4], packet2.toByteArray())