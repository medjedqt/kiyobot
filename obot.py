import discord
from discord.ext import commands
import asyncio
from kiyo import lines
from helpy import hell
from random import choice, randint, uniform
from pybooru import Danbooru
import requests
import os
import aiohttp
import io
import math
from bs4 import BeautifulSoup
from pyyoutube import Api as ytapi
from epicmodules import algorithmgodbeblessed, cloudsavedtheworld, kiyofuckingburns, dumbooruamirite, meltfuckingmeltsthankstokiyo, utilititties

intents = discord.Intents.default()
intents.members = True
helpcmd = discord.ext.commands.MinimalHelpCommand()
bot = commands.Bot(command_prefix='?',case_insensitive=True,help_command=helpcmd,intents=intents)
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
ytclient = ytapi(api_key=os.environ['YT_API'])
db = Danbooru('danbooru',username=dbname,api_key=dbkey)
queuechan = 743713887123275817
logchan = 693130723015524382
releasechan = 748084599447355523
releasehistory = []

@bot.event
async def on_ready():

	print(f'We have logged in as {bot.user}')
	bot.loop.create_task(status_task())
	bot.loop.create_task(nh_task())
	channel = bot.get_channel(logchan)
	await channel.send(content='Restarted')
	global releasehistory
	releasehistory = await bot.get_channel(releasechan).history().flatten()

async def status_task():

	while True:
		await bot.change_presence(activity=discord.Game(name="with Fira's pussy"))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Activity(name="Fira nutting to me", type=discord.ActivityType.watching))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Game(name="?help"))
		await asyncio.sleep(8)		

async def nh_task():

	await asyncio.sleep(10)
	releaselinks = []
	for things in releasehistory:
		releaselinks.append(things.content)

	while True:
		channel = bot.get_channel(releasechan)
		html = requests.get('https://nhentai.net')
		soup = BeautifulSoup(html.text, 'html.parser')
		kw = 'melty scans'
		for title in soup.find_all('div', class_="caption")[5:]:
			if kw in title.string.lower():
				url = f"https://nhentai.net{title.parent.get('href')}"
				
				if url in releaselinks:
					continue
				else:
					#await channel.send(content='Melty Scans has a new release uploaded on NHentai!')
					await channel.send(content=url)
					releaselinks.append(url)
		await asyncio.sleep(10)

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
		return
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(content="Please wait!")
	if isinstance(error, commands.NotOwner):
		await ctx.send(content="Owner only command ❌")
	channel = bot.get_channel(logchan)
	await channel.send(content=error)
	raise error

@bot.event
async def on_message(message):

	e = discord.Embed(color=0xffff00)
	if message.author.bot or message.startswith('?'):
		pass
	elif isinstance(message.channel,discord.DMChannel):
		channel = bot.get_channel(logchan)
		sender = message.author.name + " said"
		if message.attachments != []:
			attachment = message.attachments[0]
			fileurl = attachment.url
			ext = fileurl[-4:]
			async with aiohttp.ClientSession() as session:
				async with session.get(fileurl) as response:
					if response.status != 200:
						return await channel.send('Could not download file...')
					data = io.BytesIO(await response.read())
					await channel.send(file=discord.File(data, f'file{ext}'))
		e.add_field(name=sender, value=message.content)
		await channel.send(embed=e)
	await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):

	if before.author.bot or before.content == after.content or before.guild.id != 569845300244774922:
		return
	channel = bot.get_channel(logchan)
	e = discord.Embed(title=before.author.name, color=0xff0000)
	e.add_field(name="Edited", value=f'"{before.content}" to "{after.content}"')
	await channel.send(embed=e)

@bot.command(help=hell['connect'])
async def connect(ctx):

	voice = ctx.author.voice
	if voice is None:
		await ctx.send(content='Join a voice channel first')
	else:
		await voice.channel.connect()
		await ctx.send("*hacker voice* I'M IN")

@bot.command(aliases=['dc'],help=hell['disconnect'])
async def disconnect(ctx):

	if bot.voice_clients == []:
		await ctx.send(content="I'm not in a voice channel")
	else:
		await ctx.voice_client.disconnect()
		await ctx.send("bye...")

bot.add_cog(algorithmgodbeblessed.MachineLearningShit(bot))
bot.add_cog(cloudsavedtheworld.Cloudshit(bot))
bot.add_cog(utilititties.Utilities(bot, logchan))
bot.add_cog(dumbooruamirite.Danboorushit(bot, db))
bot.add_cog(kiyofuckingburns.Kiyohime(bot, db))
bot.add_cog(meltfuckingmeltsthankstokiyo.MeltyScans(bot, queuechan))

@bot.command(help=hell['ping'])
async def ping(ctx, arg1 = None):

	if arg1 is not None:
		await ctx.send(content=f'{bot.latency} seconds')
	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
