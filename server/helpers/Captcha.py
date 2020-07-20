from server.helpers.String import *
from PIL import Image, ImageDraw, ImageFont

class Captcha:
	def __init__(self, server):
		self.server = server

		self.font = ImageFont.truetype("./soopafre.ttf", 15)

	def getCaptcha(self, size):
		letter = String.randomString(size)
		img = Image.new("RGB", (62, 22), (0, 50, 0))
		draw = ImageDraw.Draw(img)
		draw.text((9, 2.5), letter, font=self.font, fill=(255, 0, 0))
		return [letter, img]