class MessageDecoder:
	@staticmethod
	def decode(channel, data):
		if len(data) < 2:
			return None
		if data == b"<policy-file-request/>\x00":
			channel.transport.write(b"<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\" /></cross-domain-policy>")
			channel.close_connection()
			return None
		else:
			return data