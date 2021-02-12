from bs4 import BeautifulSoup as bs
import discord
from discord.ext import commands, tasks
import asyncio
import os
from random import choice
import re
import dateparser
import googletrans
from gtts import gTTS
import requests
import pixivpy3
import psycopg2
from udpy import UrbanClient
import youtube_dl
from kiyo import lang

class Utilities(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.ytclient = bot.ytclient
		self.logchan = bot.logchan
		self.uclient = UrbanClient()
		self.trans = googletrans.Translator()
		#self.pixapi = pixivpy3.AppPixivAPI()
		#self.pixapi.login(os.environ['PIXIV_USER'], os.environ['PIXIV_PASS'])
		self.animelistsync.start()
		self.rsscheck.start()

	@commands.Cog.listener()
	async def on_message_edit(self, before: discord.Message, after: discord.Message):
		if before.author.bot or before.content == after.content or before.guild.id != 569845300244774922:
			return
		channel = self.bot.get_channel(self.logchan)
		e = discord.Embed(title=before.author.name, color=0xff0000)
		e.add_field(name="Edited", value=f'"{before.content}" to "{after.content}"')
		await channel.send(embed=e)
	
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.author.bot or message.content.startswith('?'):
			return
		if 'https://www.reddit.com/' in message.content and '/comments/' in message.content:
			await self.redditConverter(message)
		#if "https://" in message.content and "pixiv" in message.content and "artworks" in message.content:
		#	await self.pixivConverter(message)
		
	async def redditConverter(self, message: discord.Message):
			link = ''
			for word in message.content.split():
				if word.startswith('https://www.reddit.com/'):
					link = word.split('?')[0].strip('/')
					break
			resp = requests.get(link+'.json', headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}).json()
			if resp[0]['data']['children'][0]['data']['over_18'] and not message.channel.is_nsfw():
				return
			e = discord.Embed(title=resp[0]['data']['children'][0]['data']['title'], description=message.content, url=f"https://www.reddit.com{resp[0]['data']['children'][0]['data']['permalink']}")
			e.add_field(name='Upvotes',value=resp[0]['data']['children'][0]['data']['ups'])
			e.add_field(name='Author', value=resp[0]['data']['children'][0]['data']['author'])
			medialink = resp[0]['data']['children'][0]['data']['url_overridden_by_dest']
			vlink = None
			mediameta :dict = resp[0]['data']['children'][0]['data'].get('media_metadata')
			if medialink.startswith('https://i'):
				e.set_image(url=medialink)
			elif medialink.startswith('https://v'):
				vlink = resp[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
			elif mediameta is not None:
				imgid = list(mediameta)[0]
				imgformat = mediameta[imgid]['m'].split('/')[-1]
				e.set_image(url=f'https://i.redd.it/{imgid}.{imgformat}')
				e.description+="\n*More images in the link*"
			hooks = await message.channel.webhooks()
			if hooks == []:
				hook = await message.channel.create_webhook(name='generic hook')
			else:
				hook = hooks[0]
			files = list()
			if message.attachments == []:
				files = None
			else:
				for file in message.attachments:
					await file.save(file.filename)
					files.append(discord.File(file.filename))
			await self.redditSender(hook, e, message.author, message, files, mediameta, vlink)

	async def redditSender(self, hook: discord.Webhook, embed: discord.Embed, author: discord.Member, message: discord.Message, files: list, multi_images: dict = None, video: str = None):
		hookmsg: discord.WebhookMessage = await hook.send(embed=embed, username=author.display_name, avatar_url=author.avatar_url, files=files, wait=True)
		await message.delete()
		if video:
			await hook.send(content=video, username=author.display_name, avatar_url=author.avatar_url)
		if multi_images:
			not_timeout = True
			await hookmsg.add_reaction("◀")
			await hookmsg.add_reaction("▶")
			await hookmsg.add_reaction("❌")
			while not_timeout:
				def r_check(r: discord.Reaction, u):
					return r.message == hookmsg and not u.bot
				add = self.bot.wait_for('reaction_add', check=r_check)
				less = self.bot.wait_for('reaction_remove', check=r_check)
				done, pending = await asyncio.wait([add, less], timeout=30.0, return_when=asyncio.FIRST_COMPLETED)
				for p in pending:
					p.cancel()
				if done:
					response: discord.Reaction = done.pop().result()
					embed = response.message.embeds[0]
					image_url: str = embed.image.url
					image = image_url.strip('/').split('/')[-1].split('.')
					image_id = image[0]
					image_format = image[1]
					if response.emoji == "◀":
						i = list(multi_images).index(image_id) - 1
					elif response.emoji == "▶":
						i = list(multi_images).index(image_id) + 1
						if i == len(multi_images):
							i = 0
					elif response.emoji == "❌":
						break
					else:
						continue
					new_image = list(multi_images)[i]
					embed.set_image(url=f'https://i.redd.it/{new_image}.{image_format}')
					print("ok")
					hookmsg.edit(embed)
				break
			await hookmsg.clear_reactions()

	async def pixivConverter(self, message: discord.Message):
		art_id = int()
		for word in message.content.split():
			if word.startswith("https://") and "pixiv" in word and "artworks" in word:
				art_id = int(word.split("/")[-1])
				break
		illu = self.pixapi.illust_detail(art_id)
		e = discord.Embed(title=illu.title, description=message.content)
		e.set_author(name=illu['illust']['user']['name'])
		ext = os.path.splitext(illu['illust']['image_urls']['large'])[1]
		self.pixapi.download(illu['illust']['image_urls']['large'], name=f"piximg{ext}")
		e.set_image(url=f"attachment://piximg{ext}")
		hooks = await message.channel.webhooks()
		if hooks == []:
			hook = await message.channel.create_webhook(name='generic hook')
		else:
			hook = hooks[0]
		await hook.send(embed=e, file=discord.File(f"piximg{ext}"), username=message.author.display_name, avatar_url=message.author.avatar_url)
		files = list()
		if message.attachments == []:
			files = None
		else:
			for file in message.attachments:
				await file.save(file.filename)
				files.append(discord.File(file.filename))
			await hook.send(files=files)
		await message.delete()
		os.remove(f"piximg{ext}")

	@tasks.loop(seconds=15.0)
	async def rsscheck(self):
		tobefedsoup = requests.get("https://nyaa.si/?page=rss").text
		feed = bs(tobefedsoup, features="xml")
		for entry in feed.find_all("item"):
			for anime in self.animelist:
				if entry.guid.text == self.guid:
					return
				regexshit = re.search(anime.lower().replace(" ", "[\w\s]+"), entry.title.text.lower())
				if regexshit is not None and entry.find("nyaa:categoryId").text in ("1_2", "3_1", "4_1"):
					t = discord.utils.escape_markdown(entry.title.text)
					e = discord.Embed(title=t, description=entry.find('nyaa:size').text)
					e.add_field(name="Jump", value=f"[Go to page!]({entry.guid.text})")
					date = dateparser.parse(entry.pubDate.text)
					e.timestamp = date
					e.set_footer(text=entry.find("nyaa:category").text)
					e.set_author(name="nyaa.si", url="https://nyaa.si")
					await self.rsschan.send(embed=e)
					self.guid = feed.find_all("item")[0].guid.text
					break

	@rsscheck.before_loop
	async def beforerss(self):
		await self.bot.wait_until_ready()
		self.rsschan: discord.TextChannel = self.bot.get_channel(802132987138801705)
		self.guid = None

	@tasks.loop(seconds=60.0)
	async def animelistsync(self):
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("SELECT * FROM animelist")
		self.animelist = [_[0] for _ in cur.fetchall()]

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

	@commands.command()
	async def ytdl(self, ctx: commands.Context, link: str, *, rest: str = None):
		'''ytdl, but has max limit of 8MB'''
		if not link.startswith('http'):
			link = 'ytsearch:' + link + ' ' + rest
		async with ctx.channel.typing():
			with youtube_dl.YoutubeDL({'format': 'mp4', 'outtmpl': 'vid.%(ext)s'}) as ydl:
				ydl.download([link])
			try:
				await ctx.send(file=discord.File(f'vid.mp4'))
			except discord.HTTPException:
				await ctx.send(content="File too large")
			finally:
				os.remove(f'vid.mp4')
	
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

	def permcheck(ctx: commands.Context):
		return ctx.author.id in (230935510439297024, 550076298937237544)

	@commands.group(invoke_without_command=True)
	async def rss(self, ctx: commands.Context):
		'''shows help for rss functions'''
		if ctx.invoked_subcommand is not None:
			return
		await ctx.send_help(ctx.command)
	
	@rss.command()
	@commands.check(permcheck)
	async def add(self, ctx: commands.Context, *, title: str):
		'''adds a title to rss nyaa feed'''
		if title in self.animelist:
			return await ctx.send(content="Title already tracked")
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("INSERT INTO animelist(title) VALUES(%s);", (title,))
		cur.close()
		conn.commit()
		conn.close()
		await ctx.send(content=f"Added `{title}` into the rss filter\n(Changes may take up to a minute to take place)")

	@rss.command()
	@commands.check(permcheck)
	async def remove(self, ctx: commands.Context, *, title: str):
		'''removes a title from rss nyaa feed'''
		conn = psycopg2.connect(os.environ['DATABASE_URL'])
		cur = conn.cursor()
		cur.execute("DELETE FROM animelist WHERE title = %s;", (title,))
		delrows = cur.rowcount
		cur.close()
		conn.commit()
		conn.close()
		await ctx.send(content=f"{delrows} deleted entries\n(Changes may take up to a minute to take place)")

	@rss.command(name="list")
	async def tracklist(self, ctx: commands.Context):
		e = discord.Embed(title="nyaa.si rss filter")
		e.description = ""
		for i, anime in enumerate(self.animelist):
			e.description+=f'{i+1}. {anime}\n'
		await ctx.send(embed=e)
	
	@commands.command()
	async def translate(self, ctx: commands.Context, query: str, destination: str = 'en', source: str = 'auto'):
		res = self.trans.translate(query, destination, source)
		e = discord.Embed(title="Translator", color=0x36393F)
		e.add_field(name=f"Translated from {res.src} to {res.dest}", value=res.text)
		await ctx.send(embed=e)

def setup(bot: commands.Bot):
	bot.add_cog(Utilities(bot))
