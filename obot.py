import discord
from discord.ext import commands, tasks
import asyncio
from kiyo import lines
from random import choice, randint, uniform
from pybooru import Danbooru
import requests
import os
import aiohttp
import io
import math
import basc_py4chan
from bs4 import BeautifulSoup
from pysaucenao import SauceNao
from pyyoutube import Api as ytapi
from chemspipy import ChemSpider
from difflib import get_close_matches as auto

intents = discord.Intents.default()
intents.members = True
helpcmd = commands.DefaultHelpCommand()
helpcmd.dm_help = True
ment = discord.AllowedMentions.all()
ment.replied_user = False
bot = commands.Bot(command_prefix='?',
					case_insensitive=True,
					help_command=helpcmd,
					intents=intents,
					description=choice(lines),
					allowed_mentions=ment)
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
cskey = os.environ['CHEM_API']
bot.ytclient = ytapi(api_key=os.environ['YT_API'])
bot.db = Danbooru('danbooru',username=dbname,api_key=dbkey)
bot.cs = ChemSpider(cskey)
bot.sauce = SauceNao(api_key=os.environ['SAUCE_API'])
bot.logchan = 693130723015524382
bot.queuechan = 743713887123275817
releasechan = 748084599447355523
vrdoomchan = 804293651613745182

@bot.event
async def on_ready():

	print(f'We have logged in as {bot.user}')
	channel = bot.get_channel(bot.logchan)
	await channel.send(content='Restarted')

@tasks.loop(seconds=20)
async def status_task():

	await bot.change_presence(activity=discord.Game(name="with Fira's pussy"))
	await asyncio.sleep(20)
	await bot.change_presence(activity=discord.Activity(name="Fira nutting to me", type=discord.ActivityType.watching))
	await asyncio.sleep(20)
	await bot.change_presence(activity=discord.Game(name="?help"))

@status_task.before_loop
async def before_status():

	await bot.wait_until_ready()

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
		await asyncio.sleep(30)
		
async def vrdoom_task():

	await bot.wait_until_ready()
	threadlinks = list()
	async for things in bot.get_channel(vrdoomchan).history():
		thing: discord.Embed = things.embeds[0]
		threadlinks.append(thing.timestamp)

	while True:
		channel = bot.get_channel(vrdoomchan)
		vr = basc_py4chan.Board('vr')
		vrids = vr.get_all_thread_ids()
		for x in vrids:
			doom = vr.get_thread(x)
			if "DOOM THREAD" in doom.topic.text_comment:
				doompic = doom.topic.file.file_url
				doomurl = f"https://boards.4channel.org/vr/thread/{x}"
				doomtitle = doom.topic.subject
				doomdate = doom.topic.datetime
				e = discord.Embed(title=doomtitle, url=doomurl, color=0x9ab89f, timestamp=doomdate)
				e.set_image(url=doompic)
				if doomdate not in threadlinks:
					await channel.send(embed=e)
					threadlinks.append(doomurl)
					return
		await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx: commands.Context, error):

	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(content="Please wait!")
	elif isinstance(error, commands.NotOwner):
		await ctx.send(content="Owner only command ❌")
	elif isinstance(error, commands.UnexpectedQuoteError):
		await ctx.send(content="Clean your inputs from quotes you dirty little dirt baby")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.send(content=f"Member {error.argument} not found", allowed_mentions=discord.AllowedMentions.none())
	elif isinstance(error, commands.NSFWChannelRequired):
		await ctx.send(content="NSFW channel required.")
	elif isinstance(error, discord.HTTPException) and error.code == 413:
		await ctx.send(content="Request Entity too large")
	elif isinstance(error, commands.ConversionError):
		await ctx.send(content=error, allowed_mentions=discord.AllowedMentions.none())
	elif isinstance(error, commands.DisabledCommand):
		await ctx.send(content="Command disabled temporarily")
	elif isinstance(error, discord.Forbidden):
		await ctx.send(content="Missing perms!")
	else:
		await bot.get_channel(bot.logchan).send(content=error)
		raise error

@bot.event
async def on_message(message: discord.Message):

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

@bot.command()
async def ping(ctx: commands.Context, arg1: str = None):
	'''pong'''
	if arg1 is not None:
		await ctx.send(content=f'{round(bot.latency*1000)}ms')
	await ctx.send(content=":ping_pong: Pong!")

for filer in os.listdir('epicmodules'):
	if filer.endswith('.py'):
		bot.load_extension(f'epicmodules.{filer[:-3]}')

status_task.start()
bot.loop.create_task(nh_task())
bot.loop.create_task(vrdoom_task())

bot.run(token)
