import discord
from discord.ext import commands
import asyncio
import os
from random import choice
from gtts import gTTS
from googletrans import Translator
import requests
import urllib
from bs4 import BeautifulSoup as bs
from udpy import UrbanClient
import youtube_dl
from kiyo import lang

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ytclient = bot.ytclient
		self.logchan = bot.logchan
		self.trans = Translator()
		self.uclient = UrbanClient()

	@commands.Cog.listener()
	async def on_message_edit(self, before: discord.Message, after: discord.Message):
		if before.author.bot or before.content == after.content or before.guild.id != 569845300244774922:
			return
		channel = self.bot.get_channel(self.logchan)
		e = discord.Embed(title=before.author.name, color=0xff0000)
		e.add_field(name="Edited", value=f'"{before.content}" to "{after.content}"')
		await channel.send(embed=e)
	
	@commands.command(aliases=['nword','nw'])
	async def nwordcount(self, ctx: commands.Context):
		'''counts your racism'''
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

	@commands.command()
	async def dm(self, ctx: commands.Context, user: discord.User, *, msg: str):
		'''dms a person i guess'''
		await ctx.message.delete()
		await user.send(content=msg)
	
	@commands.command()
	async def say(self, ctx: commands.Context, *, msg: str):
		'''yes'''
		await ctx.message.delete()
		await ctx.send(content=msg, allowed_mentions=discord.AllowedMentions.none())
	
	@commands.command()
	async def tts(self, ctx: commands.Context, *, msg: str):
		'''yesser'''
		msga = await ctx.send(content=msg, tts=True)
		await msga.delete()
		await ctx.message.delete()
	
	@commands.command(aliases=['go'])
	async def google(self, ctx: commands.Context, *, query: str):
		'''google.'''
		safe = 'strict'
		if ctx.channel.is_nsfw():
			safe = 'off'
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
		r = requests.get("https://google.com/search?q="+urllib.parse.quote(query)+"&safe="+safe, headers=header)
		soup = bs(r.text, 'html.parser').find_all("div", class_="kCrYT")
		for i in soup:
			if i.a is not None and i.a['href'].startswith("/url"):
				await ctx.send(urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0])
				return
	
	@commands.command()
	async def calc(self, ctx: commands.Context, *, inp: str):
		'''It's a calculator'''
		result = eval(inp)
		await ctx.send(content=result)
	
	@commands.command(aliases=['yt'])
	async def youtube(self, ctx: commands.Context, *, words: str):
		'''Searches youtube vids'''
		results = self.ytclient.search_by_keywords(q=words,search_type='video',limit=1,count=1)
		link = f'https://youtu.be/{results.items[0].id.videoId}'
		e = await ctx.send(content=link)

	@commands.command()
	async def yeet(self, ctx: commands.Context, *emotes: discord.PartialEmoji):
		'''Posts the link to a custom emote'''
		for emote in emotes:
			await ctx.send(content=emote.url)
	
	@commands.command()
	async def pick(self, ctx: commands.Context, *arg: str):
		'''Chooses randomly from a list'''
		await ctx.send(content=choice(arg))

	@commands.command()
	async def mp3(self, ctx: commands.Context, langu: str, *, words: str):
		'''Generates an mp3 file of whatever you type'''
		if langu not in lang:
			words = langu + ' ' + words
			langu = 'en'
		tts = gTTS(words, lang=langu)
		tts.save('kiyo.mp3')
		await ctx.send(file=discord.File('kiyo.mp3'))
	
	@commands.command(aliases=['urbandictionary', 'ud'])
	async def urban(self, ctx: commands.Context, *, words: str):
		'''searches the urbandictionary'''
		try:
			udthing = self.uclient.get_definition(words)[0]
			e = discord.Embed(title=udthing.word, description=udthing.definition, color=0x441400)
			e.add_field(name='Example:', value=udthing.example)
			await ctx.send(embed=e)
		except IndexError:
			await ctx.send(content="Word doesn't exist.")
		except discord.HTTPException:
			await ctx.send(content='The definition is a fucking essay.')
	
	@commands.command(aliases=['trans'])
	async def translate(self, ctx: commands.Context, words: str, target: str = 'en', source: str = 'auto'):
		'''Translates stuff (broken for now)'''
		try:
			neword = self.trans.translate(words, dest=target, src=source)
		except ValueError:
			await ctx.send(content="Usage: `?translate 'words' destination(optional) source(optional)`")
			return
		e = discord.Embed(color=0x000055, title='Translator')
		e.add_field(name=f'Translated from {neword.src}', value=neword.text)
		await ctx.send(embed=e)

	@commands.command()
	async def ytdl(self, ctx: commands.Context, link: str, format_: str = 'best'):
		'''ytdl, but has max limit of 8MB'''
		ext = ''
		async with ctx.channel.typing():
			with youtube_dl.YoutubeDL({'format': format_}) as ydl:
				ydl.download([link])
			for file in os.listdir("./"):
				if file.endswith((".mp4", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".wmv")):
					_, ext = os.path.splitext(file)
					os.rename(file, f'vid{ext}')
			try:
				await ctx.send(file=discord.File(f'vid{ext}'))
			except discord.HTTPException:
				await ctx.send(content="File too large, consider tuning the quality.")
			os.remove(f'vid{ext}')
	
	@commands.guild_only()
	@commands.command()
	async def clone(self, ctx: commands.Context, user: discord.Member, *, message: str):
		'''Copies people or sumn idk'''
		name = user.nick
		if name is None:
			name = user.name
		hook = await ctx.channel.create_webhook(name=name)
		await hook.send(content=message, username=name, avatar_url=user.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
		await ctx.message.delete()
		await hook.delete()

	@commands.command()
	async def embed(self, ctx: commands.Context, *, words: str):
		'''Embeds whatever you say'''
		e = discord.Embed(title=ctx.author.name, description=words, color=0x523523)
		e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=e)
	
	@commands.command()
	async def poll(self, ctx: commands.Context, question: str, *choices: str):
		'''democracy'''
		if len(choices) > 9:
			await ctx.send(content="Choices can't be more than 9")
			return
		x = 0
		e = discord.Embed(title=question, color=0x2f3136)
		e.set_author(name=f'asked by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
		for choice in choices:
			x = x + 1
			e.add_field(name='Choice {}\N{variation selector-16}\N{combining enclosing keycap}'.format(x), value=choice)
		message = await ctx.send(embed=e)
		x = 0
		for choice in choices:
			x = x + 1
			await message.add_reaction('{}\N{variation selector-16}\N{combining enclosing keycap}'.format(x))

def setup(bot: commands.Bot):
	bot.add_cog(Utilities(bot))