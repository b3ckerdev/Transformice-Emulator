import re, json, urllib.request, threading
from server.helpers.String import *

class YoutubeAPI(threading.Thread):
	def __init__(self, users, channel, room, key):
		threading.Thread.__init__(self)
		self.users = users
		self.channel = channel
		self.player = channel.player
		self.room = room
		self.key = key
		data = json.loads(self.getURLContent("https://www.googleapis.com/youtube/v3/videos?id={}&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails".format(self.key)))
		if data["pageInfo"]["totalResults"] == 0:
			return
		elif data["items"][0]["snippet"]["title"] in self.room.musicList:
			self.users.sendLangueMessage(self.channel, self.player.langue.lower(), "$DejaPlaylist", [])
		elif self.parseDuration(data["items"][0]["contentDetails"]["duration"]) > 300:
			self.users.sendLangueMessage(self.channel, self.player.langue.lower(), "$ModeMusic_ErreurVideo", [])
		else:
			n = self.users.parsePlayerName(self.player)
			self.room.musicList[n] = data
			self.users.sendLangueMessage(self.channel, self.player.langue.lower(), "$ModeMusic_AjoutVideo", ["<V>{}</V>".format(len(self.room.musicList))])
			self.room.rooms.changeRoomMusic(self.room)

	def getURLContent(self, url):
		response = urllib.request.urlopen(url)
		content = response.read()
		response.close()
		return content

	def parseDuration(self, duration):
		time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
		for key, count in time.items():
			time[key] = 0 if count is None else time[key]
		return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)
