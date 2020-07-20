import discord, threading, asyncio, time, random
from discord import User
from discord.ext import commands

class Discord:
	server = None
	bot = commands.Bot(command_prefix='n!', description="")
	times = {}

	@staticmethod
	def setServer(server):
		Discord.server = server

	@staticmethod
	def run(key):
		asyncio.ensure_future(
			Discord.bot.run(key),
			loop=Discord.bot.loop
		).add_done_callback(fn)

	@staticmethod
	def genStr(size):
		string = ""
		while size > 0:
			string += random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
			size -= 1
		return string

	@bot.event
	async def on_ready():
		await Discord.bot.change_presence(activity=discord.Game(name=Discord.server.config["name"]))
		Discord.server.println("Connection successful ({}#{}).".format(Discord.bot.user.name, Discord.bot.user.discriminator), "info")

	#@bot.event
	#async def on_message(message):
	#	if message.author == Discord.bot.user:
	#		return
	#	if message.author.id in Discord.times:
	#		if (time.time() - Discord.times[message.author.id]) < 2 or "discord.gg" in message.content:
	#			await message.delete()
	#	Discord.times[message.author.id] = time.time()

	@bot.event
	async def on_member_join(ctx):
		await ctx.send("Olá! Bem-vindo(a) ao servidor oficial do {}! Leia as <#667286918043533322> para evitar futuras punições. Verifique sua conta e ganhe títulos no jogo! Vá até <#667962768179331072> e digite `n!verification Nickname#0000`.".format(Discord.server.config["name"]))

	@bot.command()
	async def stats(ctx):
		if ctx.channel.id == 699709947557969950:
			playersCount = len(list(Discord.server.users.players))
			roomsCount = len(list(Discord.server.rooms.rooms))
			accountsCount = 0
			for email, accounts in Discord.server.cache.usersByEmail.items():
				accountsCount += len(accounts)
			season = Discord.server.config["season"]
			recordPlayers = Discord.server.config["record_players_online"]
			embed = discord.Embed(title="Informações atuais do servidor", description=f"Jogadores Online: **{playersCount}**\nSalas Online: **{roomsCount}**\nContas Criadas: **{accountsCount}**\nTemporada Atual: **{season}**\nRecorde de Jogadores Online: **{recordPlayers}**\n", color=7506394)
			embed.set_footer(text=time.ctime())
			await ctx.send("Olá {}!\n".format(ctx.message.author.mention), embed=embed)

	@bot.command()
	async def verification(ctx, *args):
		if ctx.channel.id == 699709947557969950:
			if len(args) == 1:
				playerName = args[0].capitalize()
				if playerName in Discord.server.users.players:
					if playerName in Discord.server.cache.discordCodes and int(Discord.server.getTime() -  Discord.server.cache.discordCodes[playerName]["time"]) < 600:
						if Discord.server.cache.discordCodes[playerName]["changed"]:
							await ctx.send("Olá {}! A conta {} já foi verificada.".format(ctx.message.author.mention, playerName))
						elif Discord.server.cache.discordCodes[playerName]["completed"]:
							Discord.server.cache.discordCodes[playerName]["changed"] = True
							await ctx.author.edit(nick=playerName)
							await ctx.send("Obrigado {}! Sua conta foi verificada com sucesso!".format(ctx.message.author.mention, playerName))
						else:
							await ctx.send("Olá {}! O seu código de verificação é `{}`. Entre no jogo, digite `/code` e insira seu código. Ao efetuar esta verificação, volte aqui e digite `n!verification {}`.".format(ctx.message.author.mention, Discord.server.cache.discordCodes[playerName]["code"], playerName))
					else:
						code = Discord.genStr(random.randint(5, 10))
						Discord.server.cache.discordCodes[playerName] = {"code": code, "time": Discord.server.getTime(), "userID": ctx.author.id, "completed": False, "changed": False}
						await ctx.send("Olá {}! O seu código de verificação é `{}`. Entre no jogo, digite `/code` e insira seu código. Ao efetuar esta verificação, volte aqui e digite `n!verification {}`.".format(ctx.message.author.mention, code, playerName))
				else:
					await ctx.send("Olá {}! Para verificar sua conta é preciso que você esteja online em sua conta no jogo.".format(ctx.message.author.mention))

	@bot.command()
	async def mods(ctx):
		if ctx.channel.id == 699709947557969950:
			players_c = {}
			for player2 in Discord.server.users.players.values():
				if player2.privLevel > 4 and player2.privLevel < 10 and player2.privLevel != 7 and not player2.isHide:
					if not player2.langue in players_c:
						players_c[player2.langue] = []
					players_c[player2.langue].append(Discord.server.users.parsePlayerName(player2))
			msg = []
			for comm, players in players_c.items():
				msg.append("\n[`{}`] {}".format(comm.lower(), ", ".join(players)))
			embed = discord.Embed(title="Moderadores online:", description="\n".join(msg), color=7506394)
			embed.set_footer(text=time.ctime())
			await ctx.send("Olá {}!\n".format(ctx.message.author.mention), embed=embed)

	@bot.command()
	async def mapcrew(ctx):
		print(ctx.channel.id)
		if ctx.channel.id == 699709947557969950:
			players_c = {}
			for player2 in Discord.server.users.players.values():
				if player2.isMapcrew and player2.privLevel < 10 and not player2.isHide:
					if not player2.langue in players_c:
						players_c[player2.langue] = []
					players_c[player2.langue].append(Discord.server.users.parsePlayerName(player2))
			msg = []
			for comm, players in players_c.items():
				msg.append("\n[`{}`] {}".format(comm.lower(), ", ".join(players)))
			embed = discord.Embed(title="Membros da Map Crew online:", description="\n".join(msg), color=7506394)
			embed.set_footer(text=time.ctime())
			await ctx.send("Olá {}!\n".format(ctx.message.author.mention), embed=embed)
