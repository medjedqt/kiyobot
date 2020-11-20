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
from chemspipy import ChemSpider
from difflib import get_close_matches as auto

intents = discord.Intents.default()
intents.members = True
helpcmd = discord.ext.commands.MinimalHelpCommand()
bot = commands.Bot(command_prefix='?',case_insensitive=True,help_command=helpcmd,intents=intents,description=choice(lines))
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
cskey = os.environ['CHEM_API']
bot.ytclient = ytapi(api_key=os.environ['YT_API'])
bot.db = Danbooru('danbooru',username=dbname,api_key=dbkey)
bot.cs = ChemSpider(cskey)
bot.logchan = 693130723015524382
bot.queuechan = 743713887123275817
releasechan = 748084599447355523

@bot.event
async def on_ready():

	print(f'We have logged in as {bot.user}')
	channel = bot.get_channel(bot.logchan)
	await channel.send(content='Restarted')

async def status_task():

	await bot.wait_until_ready()
	while True:
		await bot.change_presence(activity=discord.Game(name="with Fira's pussy"))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Activity(name="Fira nutting to me", type=discord.ActivityType.watching))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Game(name="?help"))
		await asyncio.sleep(8)

async def nh_task():

	await bot.wait_until_ready()
	releaselinks = list()
	async for things in bot.get_channel(releasechan).history():
		releaselinks.append(things.content)

	while True:
		channel = bot.get_channel(releasechan)
		html = requests.get('https://nhentai.net')
		soup = BeautifulSoup(html.text, 'html.parser')
		kw = 'melty scans'
		for title in soup.find_all('div', class_="caption")[5:]:
			if kw in title.string.lower():
				url = f"https://nhentai.net{title.parent.get('href')}"
				if url not in releaselinks:
					await channel.send(content=url)
					releaselinks.append(url)
					queue = await bot.get_channel(bot.queuechan).history().flatten()
					queuecontent = [_.content.split(" --> ")[0][7:] for _ in queue]
					match = auto(title, queuecontent, 1, 0.7)
					if match != []:
						for item in queue:
							if match[0] in item.content:
								await bot.get_cog("Melty Scans").done(id_=item.content[3:7])
								return
					await bot.get_channel(bot.logchan).send("A release has been detected but no match has been found in queue.\nPlease use `?done` where appropriate.")
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
		return
	if isinstance(error, commands.NotOwner):
		await ctx.send(content="Owner only command ❌")
		return
	if isinstance(error, commands.UnexpectedQuoteError):
		await ctx.send(content="Clean your inputs from quotes you dirty little dirt baby")
		return
	if isinstance(error, commands.MemberNotFound):
		await ctx.send(content=f"Member {error.argument} not found")
		return
	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send(content="NSFW channel required.")
		return
	await bot.get_channel(bot.logchan).send(content=error)
	raise error

@bot.event
async def on_message(message):

	e = discord.Embed(color=0xffff00)
	if message.author.bot or message.content.startswith('?'):
		pass
	elif isinstance(message.channel,discord.DMChannel):
		channel = bot.get_channel(bot.logchan)
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

for filer in os.listdir('epicmodules'):
	if filer.endswith('.py'):
		bot.load_extension(f'epicmodules.{filer[:-3]}')

bot.loop.create_task(status_task())
bot.loop.create_task(nh_task())

@bot.command(help=hell['ping'])
async def ping(ctx, arg1 = None):

	if arg1 is not None:
		await ctx.send(content=f'{bot.latency} seconds')
	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
