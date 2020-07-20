import re, random, xml.etree.ElementTree as xml, xml.parsers.expat

class String:
	@staticmethod
	def randomString(size):
		letter = ""
		for i in range(size):
			letter += random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
		return letter

	@staticmethod
	def randomNumber(size):
		letter = ""
		for i in range(size):
			letter += random.choice(list("0123456789"))
		return letter

	@staticmethod
	def filtreChatString(string):
		if string[:1] == " ":
			string = string[1:]
		if "  " in string:
			string = string.replace("  ", " ")
		string = string.replace("\n", "\\n")
		string = string.replace("\r", "\\r")
		string = string.replace("\t", "\\t")
		string = string.replace("&amp;#", "&#")
		string = string.replace("<", "&lt;")
		return string

	@staticmethod
	def getYoutubeID(url):
		matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
		return matcher.group(1) if matcher else None

	@staticmethod
	def checkValidXML(XML):
		if re.search("ENTITY", XML) and re.search("<html>", XML):
			return False
		else:
			try:
				parser = xml.parsers.expat.ParserCreate()
				parser.Parse(XML)
				return True
			except:
				return False

	@staticmethod
	def matchPlayerName(playerName):
		valid = True
		for letter in list(playerName):
			if not letter.upper() in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ012345678_+"):
				valid = False
				break
		return valid