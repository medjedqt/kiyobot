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

intents = discord.Intents.default()
intents.members = True
helpcmd = discord.ext.commands.MinimalHelpCommand()
bot = commands.Bot(command_prefix='?',case_insensitive=True,help_command=helpcmd,intents=intents)
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)
logchan = 693130723015524382
messagechan = [612306757145853953]
releasechan = 748084599447355523
queuechan = 743713887123275817
rpslist = ['rock', 'paper', 'scissors']
gauth = GoogleAuth()
gauth.LoadCredentialsFile("auth.json")
if gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
drive = GoogleDrive(gauth)
browser = webdriver.Chrome(ChromeDriverManager().install())
funabrowse = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.cleverbot.com')
browser.execute_script('noteok()')
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
	if message.author.bot or message_text.startswith('?') or message.content in rpslist:
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

class MeltyScans(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def test(self, ctx):
		await ctx.send('still works baby')

	@commands.is_owner()
	@commands.command()
	async def betaqueue(self, ctx, nhlink, raws = 'None', doclink = 'None', entitle = 'None', *en2):

		if en2 is None:
			pass
		else:
			en2 = ' '.join(en2)
			entitle = ' '.join((entitle,en2))
		if nhlink.startswith('https://nh'):
			pass
		else:
			try:
				nhcode = int(nhlink)
			except ValueError:
				await ctx.send(content='Error: Check your input')
				return
			nhlink = f'https://nhentai.net/g/{nhcode}'
		queuechannel = bot.get_channel(queuechan)
		pastqueue = await queuechannel.history(limit=1).flatten()
		prevmessage = pastqueue[0]
		if 'MS#' not in prevmessage.content:
			queuetag = '0001'
		else:
			queuetag = int(prevmessage.content[3:7]) + 1
			queuetag = f'{queuetag:04d}'
		firstpage = requests.get(nhlink)
		soup = BeautifulSoup(firstpage.text, 'html.parser')
		nhimg = requests.get(f'{nhlink}/1')
		imgsoup = BeautifulSoup(nhimg.text, 'html.parser')
		nhimglink = imgsoup.find('section', id='image-container').a.img['src']
		imgresp = requests.get(nhimglink)
		f = open("nhimage.jpg", "wb")
		f.write(imgresp.content)
		f.close()
		orititle = soup.find(id='info').h1.get_text()
		text = f'''MS#{queuetag} **{orititle}** --> {entitle}
NH link: <{nhlink}>
raw source: <{raws}>
TL link: <{doclink}>'''
		await queuechannel.send(content=text, file=discord.File('nhimage.jpg'))

	@commands.is_owner()
	@commands.command()
	async def raw(self, ctx, id_, url):

		messages = await bot.get_channel(queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')
				for line in oldcontent:
					if 'raw' in line:
						newcontent = message.content.replace(line, f'raw source: <{url}>')
				await message.edit(content=newcontent)

	@commands.is_owner()
	@commands.command()
	async def doc(self, ctx, id_, url):

		messages = await bot.get_channel(queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')
				for line in oldcontent:
					if 'TL link' in line:
						newcontent = message.content.replace(line, f'TL link: <{url}>')
				await message.edit(content=newcontent)

	@commands.is_owner()
	@commands.command()
	async def title(self, ctx, id_, *title):

		title = ' '.join(title)
		messages = await bot.get_channel(queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				oldcontent = message.content.split('\n')[0]
				oldline = oldcontent.split(' --> ')
				newline = oldline[0] + ' --> ' + title
				newcontent = message.content.replace(oldcontent, newline)
				await message.edit(content=newcontent)
	
	@commands.is_owner()
	@commands.command()
	async def cancel(self, ctx, id_):

		messages = await bot.get_channel(queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				if message.content.endswith('~~'):
					await ctx.send(content='Doujin already cancelled')
					return
				if message.content.endswith('✅'):
					await ctx.send(content='Doujin already finished')
					return
				await message.edit(content=f'MS#{id_} ~~{message.content[8:]}~~')
	
	@commands.is_owner()
	@commands.command()
	async def done(self, ctx, id_):

		messages = await bot.get_channel(queuechan).history().flatten()
		for message in messages:
			if f'MS#{id_}' in message.content:
				if message.content.endswith('~~'):
					await ctx.send(content='Doujin already cancelled')
				elif message.content.endswith('✅'):
					await ctx.send(content='Doujin already finished')
					return
				await message.edit(content=f'{message.content} ✅')

	@commands.is_owner()
	@commands.command()
	async def ownershiptest(self, ctx):
		await ctx.send('what')
	
class Kiyohime(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help=hell['burn'])
	async def burn(self, ctx):

		e=discord.Embed(color=0xff0000)
		e.set_image(url=choice(burnlist))
		await ctx.send(embed=e)

	@commands.command(help=hell['step'])
	async def step(self, ctx):

		e=discord.Embed(color=0xffff00)
		e.set_image(url="https://cdn.discordapp.com/attachments/611844054669328394/635200592364699649/IMG_20191020_024438.JPG")
		await ctx.send(embed=e)
	
	@commands.command(aliases=['k','kiyohime'], help=hell['kiyo'])
	async def kiyo(self, ctx):

		x = []
		page = randint(1,15)
		posts = db.post_list(tags='kiyohime_(fate/grand_order)',page=page,limit=100)
		for post in posts:
			try:
				fileurl = post['file_url']
			except:
				fileurl = 'https://danbooru.donmai.us' + post['source']
			x.append(fileurl)
		e = discord.Embed(color=0x00ff00)
		e.set_image(url=choice(x))
		await ctx.send(embed=e)
	
class Danboorushit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help=hell['latest'])
	async def latest(self, ctx, key=None, *tag):

		if key is None:
			tag="kiyohime_(fate/grand_order)"
		else:
			tag = '_'.join(tag)
			tag = key + '_' + tag
		posts = db.post_list(tags=tag, page=1, limit=1)
		for post in posts:
			try:
				fileurl = post['file_url']
			except:
				fileurl = 'https://danbooru.donmai.us' + post['source']
		e = discord.Embed(title="Latest", color=0x00FF00)
		e.set_image(url=fileurl)
		await ctx.send(embed=e)
	
	@commands.command(aliases=['danbooru','d'],help=hell['danbooru'])
	async def dan(self, ctx, *tag):

		x = []
		newtag = '_'.join(tag)
		page = randint(1,5)
		try:
			posts = db.post_list(tags=newtag,page=page,limit=5)
			for post in posts:
				try:
					fileurl = post['file_url']
				except:
					fileurl = 'https://danbooru.donmai.us' + post['source']
				x.append(fileurl)
			e = discord.Embed(color=0x0000ff)
			e.set_image(url=choice(x))
			await ctx.send(embed=e)
		except:
			await ctx.send(content="Can't find image! Please enter in this format `character name (series)`")

	@commands.command(help=hell['multi'])
	async def multi(self, ctx, *tag):

		x=[]
		tag = ' '.join(tag)
		page = randint(1,5)
		try:
			posts = db.post_list(tags=tag,page=page,limit=5)
			for post in posts:
				try:
					fileurl = post['file_url']
				except:
					fileurl = 'https://danbooru.donmai.us' + post['source']
				x.append(fileurl)
			e = discord.Embed(color=0x00FFBE)
			for poop in x:
				e.set_image(url=poop)
				await ctx.send(embed=e)
		except:
			await ctx.send(content="Some shit broke. Also firara is gay")

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

	@commands.command(hell['dm'])
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

class Cloudshit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['u','up'],help=hell['upload'])
	async def upload(self, ctx,title=None):

		try:
			attachment =ctx.message.attachments[0]
			fileurl=attachment.url
			if fileurl.find('/'):
				name=fileurl.rsplit('/',1)[1]
				exname, ext = os.path.splitext(name)
			r=requests.get(fileurl,stream=True)
			if title is None:
				newname = exname+ext
			else:
				newname = title+ext
			if r.status_code==200:
				with open(newname,'wb') as f:
					r.raw.decode_content=True
					shutil.copyfileobj(r.raw,f)
		except:
			await ctx.send(content="Attach a file!")
			return
		file1 = drive.CreateFile()
		file1.SetContentFile(newname)
		file1.Upload()
		await ctx.send(content="Uploaded as {0}".format(newname))
		os.remove(newname)

	@commands.command(aliases=['dl','down'], help=hell['download'])
	async def download(self, ctx,file):

		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
		for file2 in file_list:
			title = file2['title']
			name, _ = os.path.splitext(title)
			file_notthere = True
			if file in name:
				file1 = drive.CreateFile({'id':file2['id']})
				file1.GetContentFile(title)
				await ctx.send(file=discord.File(title))
				os.remove(title)
				file_notthere = False
				break
		if file_notthere:
			await ctx.send("Can't find file :c")

	@commands.command(aliases=['ls'], help=hell['list'])
	async def list(self, ctx):

		e = discord.Embed(title='Cloud Files',color=0x00ffff)
		file_list = drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
		for file1 in file_list:
			_, ext = os.path.splitext(file1['title'])
			next = tension.Ext(ext)
			e.add_field(name=file1['title'],value=next,inline=False)
		await ctx.send(embed=e)

	@commands.command(help=hell['trash'])
	async def trash(self, ctx, filename):

		file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
		for file in file_list:
			title = file['title']
			name, _ = os.path.splitext(title)
			if filename in name:
				actual_file = drive.CreateFile({'id':file['id']})
				actual_file.Trash()
				await ctx.send(content='Binned {0}'.format(file['title']))

class MachineLearningShit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def word(self, ctx):

		r = requests.get('https://www.thisworddoesnotexist.com/')
		soup = BeautifulSoup(r.text, 'html.parser')
		defword = soup.find(id='definition-word').string
		deflink = soup.find(id='link-button-a')['href']
		defgrammar = soup.find(id='definition-pos').string
		defgrammar = defgrammar.replace('"','').strip()
		defex = soup.find(id='definition-example').string
		defdef = soup.find(id='definition-definition').string
		defdesc = defgrammar + ' ' + defdef
		e = discord.Embed(title=defword, url=deflink,color=0x002258)
		e.add_field(name=defdesc, value=defex)
		e.set_footer(text='Powered by This Word Does Not Exist',icon_url='https://www.thisworddoesnotexist.com/favicon-32x32.png')
		await ctx.send(embed=e)

	@commands.command()
	async def wordcloud(self, ctx, chanlimit=100, max=100):

		def getFrequencyDictForText(sentence):
			fullTermsDict = multidict.MultiDict()
			tmpDict = {}

			for text in sentence.split(" "):
				if text.startswith(('.','f.','!','<','-','?','$','_',':')):
					continue
				if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
					continue
				val = tmpDict.get(text, 0)
				tmpDict[text.lower()] = val + 1
			for key in tmpDict:
				fullTermsDict.add(key, tmpDict[key])
			return fullTermsDict

		messages = []
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.permissions_for(ctx.guild.me).read_messages:
				async for stuff in channel.history(limit=chanlimit):
					messages.append(stuff.content)
		text = ' '.join(messages)
		wordcloud = WordCloud(max_words=max,width=1920, height=1080, min_word_length=2).generate_from_frequencies(getFrequencyDictForText(text))
		wordcloud.to_file('wc.png')
		await ctx.send(file=discord.File('wc.png', filename='wordcloud.png'))

	@commands.command()
	async def chat(self, ctx, *question: str):

		async with ctx.channel.typing():
			q = []
			for word in question:
				if word.startswith('<@'):
					word = re.sub('[^0-9]', '', word)
					word = bot.get_user(int(word)).name
				if word.startswith('<#'):
					word = re.sub('[^0-9]', '', word)
					word = bot.get_channel(int(word)).name
				if word.startswith('<:') or word.startswith('<a:') or word.startswith(':'):
					continue
				q.append(word)
			q = ' '.join(q)
			inputbox = browser.find_element_by_name('stimulus')
			inputbox.clear()
			inputbox.send_keys(q)
			inputbox.send_keys(Keys.RETURN)
			await asyncio.sleep(5)
			response = browser.find_element_by_xpath("//p[@id='line1']/span")
			await ctx.send(content=response.text)

bot.add_cog(Cloudshit(bot))
bot.add_cog(Utilities(bot))
bot.add_cog(Danboorushit(bot))
bot.add_cog(Kiyohime(bot))
bot.add_cog(MeltyScans(bot))

@bot.command(help=hell['ping'])
async def ping(ctx, arg1 = None):

	if arg1 is not None:
		await ctx.send(content=f'{bot.latency} seconds')
	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
