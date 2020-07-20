class MessageEncoder:
	@staticmethod
	def writeRequested(channel, data):
		channel.transport.write(data)