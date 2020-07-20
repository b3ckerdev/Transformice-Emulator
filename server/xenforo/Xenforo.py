class Xenforo:
	def __init__(self, server):
		self.server = server

	def createUser(self, playerID, playerName):
		pool = self.server.database.execute("INSERT INTO xf_user (user_id, username, email, language_id, style_id, timezone, user_group_id, secondary_group_ids, permission_combination_id, secret_key, register_date) VALUES (%s, %s, '', 0, 0, 'America/Brasilia', 2, 2, 3, '', %s)", (playerID, playerName, int(self.server.getTime())))
		pool = self.server.database.execute("INSERT INTO xf_user_option (user_id) VALUES (%s)", (playerID,))
		pool = self.server.database.execute("INSERT INTO xf_user_privacy (user_id) VALUES (%s)", (playerID,))
		pool = self.server.database.execute("INSERT INTO xf_user_profile (user_id) VALUES (%s)", (playerID,))
		self.server.database.commitAll()