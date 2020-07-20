import zlib, random
from network.packet.ByteArray import *

class PCaptcha:
	C, CC = 26, 20

	@staticmethod
	def parse(users, channel, packet, packetID):
		if len(users.server.cache.captchaCaches) >= 100:
			letter = random.choice(list(users.server.cache.captchaCaches))
			img = users.server.cache.captchaCaches[letter]
		else:
			letter, img = users.server.captcha.getCaptcha(4)
			users.server.cache.captchaCaches[letter] = img

		channel.player.captcha = letter.upper()

		width, height = img.size
		pixelsCount = 0

		pixels = ByteArray()
		p2 = ByteArray()
		p2.writeByte(0)
		p2.writeShort(width)
		p2.writeShort(height)

		for row in range(height):
			for col in range(width):
				pix = img.getpixel((col, row))
				pixels.writeUnsignedByte(pix[0])
				pixels.writeUnsignedByte(pix[1])
				pixels.writeUnsignedByte(pix[2])
				pixels.writeUnsignedByte(0)
				pixelsCount += 1

		p2.writeShort(pixelsCount)
		p2.writeBytes(pixels.toByteArray())

		zlibCompress = zlib.compress(p2.toByteArray())

		p3 = ByteArray()
		p3.writeInt(len(zlibCompress))
		p3.writeBytes(zlibCompress)

		users.sendPacket(channel, [26, 20], p3.toByteArray())