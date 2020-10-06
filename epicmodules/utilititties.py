import discord
from discord.ext import commands
import asyncio
from googlesearch import search
import os
from random import choice
from gtts import gTTS
from googletrans import Translator
from udpy import UrbanClient
import youtube_dl
from kiyo import lang
from helpy import hell

trans = Translator()
uclient = UrbanClient()

class Utilities(commands.Cog):
	def __init__(self, bot, ytclient, logchan):
		self.bot = bot
		self.ytclient = ytclient
		self.logchan = logchan

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.author.bot or before.content == after.content or before.guild.id != 569845300244774922:
			return
		channel = self.bot.get_channel(self.logchan)
		e = discord.Embed(title=before.author.name, color=0xff0000)
		e.add_field(name="Edited", value=f'"{before.content}" to "{after.content}"')
		await channel.send(embed=e)
	
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
	
	@commands.command(aliases=['yt'], help=hell['youtube'])
	async def youtube(self, ctx, *words):

		words = ' '.join(words)
		results = self.ytclient.search_by_keywords(q=words,search_type='video',limit=1,count=1)
		await ctx.send(content=f'https://youtu.be/{results.items[0].id.videoId}')

	@commands.command(help=hell['yeet'])
	async def yeet(self, ctx, *emotes: discord.PartialEmoji):

		for emote in emotes:
			await ctx.send(content=emote.url)
	
	@commands.command(help=hell['pick'])
	async def pick(self, ctx, *arg):

		await ctx.send(content=choice(arg))

	@commands.command(help=hell['mp3'])
	async def mp3(self, ctx, langu, *words):

		words = ' '.join(words)
		if langu not in lang:
			words = langu + ' ' + words
			langu = 'en'
		tts = gTTS(words, lang=langu)
		tts.save('kiyo.mp3')
		await ctx.send(file=discord.File('kiyo.mp3'))
	
	@commands.command(aliases=['urbandictionary', 'urban'],help=hell['ud'])
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
	
	@commands.command(aliases=['trans'],help=hell['translate'])
	async def translate(self, ctx, words, target='en', source='auto'):

		try:
			neword = trans.translate(words, dest=target, src=source)
		except ValueError:
			await ctx.send(content="Usage: `.translate 'words' destination(optional) source(optional)`")
			return
		e = discord.Embed(color=0x000055, title='Translator')
		e.add_field(name=f'Translated from {neword.src}', value=neword.text)
		await ctx.send(embed=e)

	@commands.command(help=hell['ytdl'])
	async def ytdl(self, ctx, link):

		fformat = ''
		async with ctx.channel.typing():
			with youtube_dl.YoutubeDL({}) as ydl:
				ydl.download([link])
			for file in os.listdir("./"):
				if file.endswith((".mp4", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".wmv")):
					_, fformat = os.path.splitext(file)
					os.rename(file, f'vid{fformat}')
			await ctx.send(file=discord.File(f'vid{fformat}'))
			os.remove(f'vid{fformat}')
	
	@commands.command(help=hell['clone'])
	async def clone(self, ctx, user: discord.Member, *message):

		message = ' '.join(message)
		hook = await ctx.guild.webhooks()
		hook = hook[0]
		await hook.send(content=message, username=user.nick, avatar_url=user.avatar_url)

	@commands.command(help=hell['embed'])
	async def embed(self, ctx, *words):

		words = ' '.join(words)
		e = discord.Embed(title=ctx.author.name, description=words, color=0x523523)
		e.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=e)
	
	@commands.command(help=hell['poll'])
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
