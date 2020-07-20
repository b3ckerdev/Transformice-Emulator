import threading, mysql.connector
from mysql.connector import pooling

class Database:
	def __init__(self, server):
		self.server = server

		self.dbs = {}
		self.source = None
		self.last_pool = 0
		
	def connect(self):
		self.source = mysql.connector.pooling.MySQLConnectionPool(
			pool_name=self.server.config["database"]["pool_name"],
			pool_size=self.server.config["database"]["pool_size"],
			pool_reset_session=self.server.config["database"]["pool_reset_session"],
			host=self.server.config["database"]["host"],
			database=self.server.config["database"]["database"],
			user=self.server.config["database"]["user"],
			password=self.server.config["database"]["password"]
		)
		for pool in range(self.server.config["database"]["pool_size"]):
			connection = self.source.get_connection()
			self.dbs[pool] = {
				"connection": connection,
				"cursor": connection.cursor(buffered=True, dictionary=True)
			}
		return True

	def execute(self, query, d=()):
		pool = self.last_pool
		if not self.dbs[pool]["connection"].is_connected():
			self.dbs[pool]["connection"].reconnect(attempts=5, delay=3)
		self.dbs[pool]["cursor"].execute(query, d)
		if self.last_pool == self.server.config["database"]["pool_size"]-1:
			self.last_pool = 0
		else:
			self.last_pool += 1
		return pool

	def fetchone(self, pool):
		return self.dbs[pool]["cursor"].fetchone()

	def fetchall(self, pool):
		return self.dbs[pool]["cursor"].fetchall()

	def commit(self, pool):
		for pool, q in self.dbs.items():
			q["connection"].commit()
		#return self.dbs[pool]["connection"].commit()

	def commitAll(self):
		for pool, q in self.dbs.items():
			q["connection"].commit()