import discord
from discord.ext import commands
import asyncio
from kiyo import burnlist, lines, lang
from random import choice, randint, uniform
from pybooru import Danbooru
import requests
import shutil
import os
from helpy import hell
import tension
from googlesearch import search
import aiohttp
import io
import math
import pydrive2
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from bs4 import BeautifulSoup
import youtube_dl
import multidict
import re
from wordcloud import WordCloud
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from googletrans import Translator
from udpy import UrbanClient
from gtts import gTTS
from pyyoutube import Api as ytapi
from epicmodules import algorithmgodbeblessed, cloudsavedtheworld, kiyofuckingburns, dumbooruamirite, meltfuckingmeltsthankstokiyo

intents = discord.Intents.default()
intents.members = True
helpcmd = discord.ext.commands.MinimalHelpCommand()
bot = commands.Bot(command_prefix='?',case_insensitive=True,help_command=helpcmd,intents=intents)
token = os.environ['BOT_TOKEN']
logchan = 693130723015524382
messagechan = [612306757145853953]
releasechan = 748084599447355523
trans = Translator()
uclient = UrbanClient()
ytclient = ytapi(api_key=os.environ['YT_API'])
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

	message_text = message.content.upper()
	luck = uniform(0, 1.0)
	e = discord.Embed(color=0xffff00)
	if message.author.bot or message_text.startswith('?'):
		pass
	elif 'CHEATING' in message_text:
		await message.channel.trigger_typing()
		await asyncio.sleep(3)
		await message.channel.send('Do I smell a liar in here?')
	elif message.author.id == 293395455830654977 and luck >= 0.85 and message.guild.id == 569845300244774922:
		await message.add_reaction('❤️')
	elif bot.user.mentioned_in(message):
		if message.author.id == 293395455830654977 and luck >= 0.97:
			e.set_image(url="https://cdn.discordapp.com/attachments/569845300244774924/692219666478923776/23a8b2e1-21d4-4dac-84ba-1128207f0e30.png")
			await message.channel.send(embed=e)
		else:
			await message.channel.send(choice(lines))
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

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['nword','nw'],help=hell['nwordcount'])
	async def nwordcount(self, ctx):

		i=1
		n1counter = 0
		n2counter = 0
		keyword1 = 'NIGGER'
		keyword2 = 'NIGGA'
		mess = "stalking."
		mes = await ctx.send(content='stalking')
		while i <5: 
			await mes.edit(content=mess)
			mess = mess + "."
			await asyncio.sleep(1)
			i += 1
		async with ctx.channel.typing():
			async for message in ctx.channel.history(limit=5000):
				if message.author.id == ctx.message.author.id:
					message_text = message.content.upper()
					if keyword1 in message_text:
						n1counter += 1
					if keyword2 in message_text:
						n2counter += 1
		await mes.edit(content='Done!')
		await ctx.send(content='According to my stalking, %s have said the soft n-word %d times and the hard n-word %d times in the last 5000 messages' % (ctx.author.mention, n2counter, n1counter))

	@commands.command(help=hell['dm'])
	async def dm(self, ctx,user: discord.User, msg):
	
		await ctx.message.delete()
		await user.send(content=msg)
	
	@commands.command(help=hell['say'])
	async def say(self, ctx, msg: str, time=5, count=1):

		await ctx.message.delete()
		if (time > 86400 or count > 100):
			await ctx.send(content="Too long, I might die by then")
			await ctx.send(content="tl;dr: " + msg)
			return

		while True:
			await ctx.send(content=msg)
			await asyncio.sleep(time)
			count = count - 1
			if count == 0:
				break
	
	@commands.command(help=hell['tts'])
	async def tts(self, ctx, *msg):

		msg = ' '.join(msg)
		msga = await ctx.send(content=msg, tts=True)
		await msga.delete()
		await ctx.message.delete()
	
	@commands.command(help=hell['google'])
	async def google(self, ctx,*query):

		query = ''.join(query)
		for result in search(query, tld='com', num=1, stop=1, pause=2):
			await ctx.send(result)
	
	@commands.command(help=hell['calc'])
	async def calc(self, ctx, *inp):

		inp = ' '.join(inp)
		result = eval(inp)
		await ctx.send(content=result)
	
	@commands.command(aliases=['yt'])
	async def youtube(self, ctx, *words):

		words = ' '.join(words)
		results = ytclient.search_by_keywords(q=words,search_type='video',limit=1,count=1)
		await ctx.send(content=f'https://youtu.be/{results.items[0].id.videoId}')

	@commands.command()
	async def yeet(self, ctx, *emotes: discord.PartialEmoji):

		for emote in emotes:
			await ctx.send(content=emote.url)
	
	@commands.command()
	async def pick(self, ctx, *arg):

		await ctx.send(content=choice(arg))

	@commands.command()
	async def mp3(self, ctx, langu, *words):

		words = ' '.join(words)
		if langu not in lang:
			words = langu + ' ' + words
			langu = 'en'
		tts = gTTS(words, lang=langu)
		tts.save('kiyo.mp3')
		await ctx.send(file=discord.File('kiyo.mp3'))
	
	@commands.command(aliases=['urbandictionary', 'urban'])
	async def ud(self, ctx, *words):

		words = ' '.join(words)
		try:
			udthing = uclient.get_definition(words)[0]
			e = discord.Embed(title=udthing.word, description=udthing.definition, color=0x441400)
			e.add_field(name='Example:', value=udthing.example)
			await ctx.send(embed=e)
		except IndexError:
			await ctx.send(content="Word doesn't exist.")
		except discord.HTTPException:
			await ctx.send(content='The definition is a fucking essay.')
	
	@commands.command(aliases=['trans'])
	async def translate(self, ctx, words, target='en', source='auto'):

		try:
			neword = trans.translate(words, dest=target, src=source)
		except ValueError:
			await ctx.send(content="Usage: `.translate 'words' destination(optional) source(optional)`")
			return
		e = discord.Embed(color=0x000055, title='Translator')
		e.add_field(name='Translated from {}'.format(neword.src), value=neword.text)
		await ctx.send(embed=e)

	@commands.command()
	async def ytdl(self, ctx, link):

		format = ''
		async with ctx.channel.typing():
			with youtube_dl.YoutubeDL({}) as ydl:
				ydl.download([link])
			for file in os.listdir("./"):
				if file.endswith((".mp4", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".wmv")):
					_, format = os.path.splitext(file)
					os.rename(file, f'vid{format}')
			await ctx.send(file=discord.File(f'vid{format}'))
			os.remove(f'vid{format}')
	
	@commands.command()
	async def clone(self, ctx, user: discord.Member, *message):

		message = ' '.join(message)
		hook = await ctx.guild.webhooks()
		hook = hook[0]
		await hook.send(content=message, username=user.nick, avatar_url=user.avatar_url)

	@commands.command()
	async def embed(self, ctx, *words):

		words = ' '.join(words)
		e = discord.Embed(title=ctx.author.name, description=words, color=0x523523)
		e.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=e)
	
	@commands.command()
	async def poll(self, ctx, question, *choices):

		if len(choices) > 9:
			await ctx.send(content="Choices can't be more than 9")
			return
		x = 0
		e = discord.Embed(title=question, color=0x019901)
		e.set_author(name=f'asked by {ctx.author.nick}', icon_url=ctx.author.avatar_url)
		for choice in choices:
			x = x + 1
			e.add_field(name='Choice {}\N{variation selector-16}\N{combining enclosing keycap}'.format(x), value=choice)
		message = await ctx.send(embed=e)
		x = 0
		for choice in choices:
			x = x + 1
			await message.add_reaction('{}\N{variation selector-16}\N{combining enclosing keycap}'.format(x))

bot.add_cog(algorithmgodbeblessed.MachineLearningShit(bot))
bot.add_cog(cloudsavedtheworld.Cloudshit(bot))
bot.add_cog(Utilities(bot))
bot.add_cog(dumbooruamirite.Danboorushit(bot))
bot.add_cog(kiyofuckingburns.Kiyohime(bot))
bot.add_cog(meltfuckingmeltsthankstokiyo.MeltyScans(bot))

@bot.command(help=hell['ping'])
async def ping(ctx, arg1 = None):

	if arg1 is not None:
		await ctx.send(content=f'{bot.latency} seconds')
	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
