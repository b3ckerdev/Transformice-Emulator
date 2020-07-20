class Langues:
	def __init__(self):
		self.langues = {}
		self.langues[0] = "EN"
		self.langues[1] = "FR"
		self.langues[2] = "RU"
		self.langues[3] = "BR"
		self.langues[4] = "ES"
		self.langues[5] = "CN"
		self.langues[6] = "TR"
		self.langues[7] = "VK"
		self.langues[8] = "PL"
		self.langues[9] = "HU"
		self.langues[10] = "NL"
		self.langues[11] = "RO"
		self.langues[12] = "ID"
		self.langues[13] = "DE"
		self.langues[14] = "E2"
		self.langues[15] = "AR"
		self.langues[16] = "PH"
		self.langues[17] = "LT"
		self.langues[18] = "JP"
		self.langues[19] = "CH"
		self.langues[20] = "FI"
		self.langues[21] = "CZ"
		self.langues[22] = "SK"
		self.langues[23] = "HR"
		self.langues[24] = "BU"
		self.langues[25] = "LV"
		self.langues[26] = "HE"
		self.langues[27] = "IT"
		self.langues[29] = "ET"
		self.langues[30] = "AZ"
		self.langues[31] = "PT"

	def get(self):
		return self.langues

	def checkExistLangueStr(self, langueStr):
		for id, langue in self.langues.items():
			if langue.lower() == langueStr.lower():
				return True
		return False

	def getLangue(self, langueByte):
		return self.langues[langueByte]

	def getLangueByName(self, langue):
		for langueID, l in self.langues.items():
			if l.lower() == langue.lower():
				return langueID
		return 0