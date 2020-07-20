from network.packet.ByteArray import *

class PacketEncryption:
	def __init__(self, packetManage, users):
		self.users = users
		self.packetManage = packetManage

		self.keysCache = {}

	def bitMask(self, arg1):
		return (self.u32(arg1) + 0x80000000) % 0x100000000 - 0x80000000
    
	def u32(self, arg1):
		return arg1 & 0xffffffff

	def getKeys(self, char, keys):
		if char in self.keysCache:
			return self.keysCache[char]
		loc3 = 0
		loc4 = len(keys)
		loc5 = len(char)
		loc6 = 5381
		while loc3 < loc4:
			loc6 = self.bitMask((loc6 << 5) + loc6 + keys[loc3] + ord(char[loc3 % loc5]))
			loc3 += 1
		loc3 = 0
		self.keysCache[char] = [0] * loc4
		while loc3 < loc4:
			loc6 ^= self.bitMask(loc6 << 13)
			loc6 ^= self.bitMask(loc6 >> 17)
			loc6 ^= self.bitMask(loc6 << 5)
			self.keysCache[char][loc3] = int(loc6)
			loc3 += 1
		return self.keysCache[char]

	def xxtea_decrypt(self, v, k):
		_DELTA = 0x9E3779B9
		n = len(v) - 1
		z = v[n]
		y = v[0]
		q = 6 + 52 // (n + 1)
		sum = (q * _DELTA) & 0xffffffff
		while (sum != 0):
			e = sum >> 2 & 3
			for p in range(n, 0, -1):
				z = v[p - 1]
				v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
				y = v[p]
			z = v[n]
			v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
			y = v[0]
			sum = (sum - _DELTA) & 0xffffffff
		return v

	def identification(self, packet, packetID):
		datas = []
		count = packet.readUnsignedShort()
		for x in range(count):
			datas.append(packet.readUnsignedInt())
		datas = self.xxtea_decrypt(datas, self.getKeys("identification", self.users.server.config["protection"]["packetKeys"]))
		packet2 = ByteArray()
		for data in datas:
			packet2.writeInt(data)
		return packet2

	def msg(self, packet, packetID):
		keys = self.getKeys("msg", self.users.server.config["protection"]["packetKeys"])
		packet2 = ByteArray()
		while packet.bytesAvailable():
			packetID = (packetID + 1) % len(keys)
			packet2.write(chr((packet.readByte() ^ keys[packetID]) & 255).encode())
		return packet2