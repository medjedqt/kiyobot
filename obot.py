import discord
import asyncio
from kiyo import burnlist, lines, rpsfunc, nh_check
from random import choice, randint, uniform
from discord.ext.commands import CommandNotFound,MissingRequiredArgument,CommandOnCooldown,cooldown,Bot
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
#from mathe import calculate
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
import math
from googletrans import Translator


bot = Bot(command_prefix='?',case_insensitive=True,help_command=None)
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)
logchan = 693130723015524382
messagechan = [612306757145853953]
releasechan = 748084599447355523
rpslist = ['rock', 'paper', 'scissors']
gauth = GoogleAuth()
gauth.LoadCredentialsFile("auth.json")
if gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
drive = GoogleDrive(gauth)
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.cleverbot.com')
browser.execute_script('noteok()')
trans = Translator()
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

	releaselinks = []
	for things in releasehistory:
		releaselinks.append(things.content)

	while True:
		channel = bot.get_channel(releasechan)
		html = requests.get('https://nhentai.net')
		soup = BeautifulSoup(html.text, 'html.parser')
		kw = 'melty scans'
		for title in soup.find_all('div', class_="caption")[5:16]:
			if kw in title.string.lower():
				url = f"https://nhentai.net{title.parent.get('href')}"
				
				if url in releaselinks:
					continue
				else:
					#await channel.send(content='Melty Scans has a new release uploaded on NHentai!')
					await channel.send(content=url)
					releaselinks.append(url)
		await asyncio.sleep(20)

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, CommandNotFound):
		return
	if isinstance(error, MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
		return
	if isinstance(error, CommandOnCooldown):
		await ctx.send(content="Please wait!")
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

@bot.command(help=hell['burn'])
async def burn(ctx):

	e=discord.Embed(color=0xff0000)
	e.set_image(url=choice(burnlist))
	await ctx.send(embed=e)

@bot.command(help=hell['step'])
async def step(ctx):

	e=discord.Embed(color=0xffff00)
	e.set_image(url="https://cdn.discordapp.com/attachments/611844054669328394/635200592364699649/IMG_20191020_024438.JPG")
	await ctx.send(embed=e)

@bot.command(aliases=['nword','nw'],help=hell['nwordcount'])
async def nwordcount(ctx):
	
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

@bot.command(hell['dm'])
async def dm(ctx,user: discord.User, msg):
	
	target = bot.get_user(user.id)
	await ctx.message.delete()
	await target.send(content=msg)

@bot.command(aliases=['k','kiyohime'], help=hell['kiyo'])
async def kiyo(ctx):

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

@bot.command(help=hell['latest'])
async def latest(ctx, key=None, *tag):

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

@bot.command(aliases=['danbooru','d'],help=hell['danbooru'])
async def dan(ctx, *tag):

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

@bot.command(help=hell['multi'])
async def multi(ctx, *tag):

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

@bot.command(aliases=['u','up'],help=hell['upload'])
async def upload(ctx,title=None):

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
	file1 = drive.CreateFile()
	file1.SetContentFile(newname)
	file1.Upload()
	await ctx.send(content="Uploaded as {0}".format(newname))
	os.remove(newname)

@bot.command(aliases=['dl','down'], help=hell['download'])
async def download(ctx,file):

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

@bot.command(aliases=['ls'], help=hell['list'])
async def list(ctx):

	e = discord.Embed(title='Cloud Files',color=0x00ffff)
	file_list = drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
	for file1 in file_list:
		_, ext = os.path.splitext(file1['title'])
		next = tension.Ext(ext)
		e.add_field(name=file1['title'],value=next,inline=False)
	await ctx.send(embed=e)

@bot.command(help=hell['trash'])
async def trash(ctx, filename):

	file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
	for file in file_list:
		title = file['title']
		name, _ = os.path.splitext(title)
		if filename in name:
			actual_file = drive.CreateFile({'id':file['id']})
			actual_file.Trash()
			await ctx.send(content='Binned {0}'.format(file['title']))

@bot.command(help=hell['connect'])
async def connect(ctx):

	voice = ctx.author.voice
	if voice == None:
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

@bot.command(help=hell['say'])
async def say(ctx, msg: str, time=5, count=1):

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

@bot.command(help=hell['tts'])
async def tts(ctx, *msg):

	msg = ' '.join(msg)
	msga = await ctx.send(content=msg, tts=True)
	await msga.delete()
	await ctx.message.delete()

@bot.command(help=hell['google'])
async def google(ctx,*query):

	query = ''.join(query)
	for result in search(query, tld='com', num=1, stop=1, pause=2):
		await ctx.send(result)

@bot.command(help=hell['calc'])
#async def calc(ctx, func, arg=None, arg2=None):
async def calc(ctx, *inp):
	#function = calculate[func]
	#if arg2 is None:
	#	result = function(int(arg))
	#else:
	#	result = function(int(arg),int(arg2))
	inp = ' '.join(inp)
	result = eval(inp)
	await ctx.send(content=result)

@bot.command()
async def rps(ctx, userid, move):

	if isinstance(ctx.channel,discord.DMChannel) and move in rpslist:
		target = bot.get_user(int(userid))
		await ctx.send(content=f"Challenged {target.name}")
		await target.send(content=f'{ctx.author.name} challenged you to a rock paper scissors! Reply with your move (Rock/Paper/Scissors)')
	elif isinstance(ctx.channel,discord.DMChannel) and move not in rpslist:
		await ctx.send(content='Not a valid move')
	else:
		await ctx.send(content='You have to use this command in my DM')
	
	def check(victim):
		if victim.author.name == target.name and isinstance(victim.channel, discord.DMChannel):
			return True
		else:
			return False
	
	msg = await bot.wait_for('message', check=check)
	xmove = msg.content
	if xmove in rpslist:
		result = rpsfunc(move, xmove)
		if result == 'tie':
			await ctx.send(content="It's a tie!")
			await target.send(content="It's a tie!")
		elif result == 'p1loss':
			await ctx.send(content="You've lost!")
			await target.send(content="You've won!")
		elif result == 'p1win':
			await ctx.send(content="You've won!")
			await target.send(content="You've lost!")
	else:
		await target.send(content='Invalid move! Game cancelled')
		await ctx.send(content='Opponent made an invalid move. Game is cancelled')

@bot.command()
async def word(ctx):

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

@bot.command()
async def sing(ctx, link):

	if bot.voice_clients == []:
		voice = ctx.author.voice
		await voice.channel.connect()
	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("Wait for the current playing music end or use the 'stop' command")
		return
	await ctx.send("Getting everything ready, playing audio soon")
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([link])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio("song.mp3"))
	voice.volume = 100
	voice.is_playing()

@bot.command()
async def wordcloud(ctx, chanlimit=100, max=100):

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

@bot.command()
async def chat(ctx, *question: str):

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

@bot.command()
async def poll(ctx, question, *choices):

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

@bot.command()
async def clone(ctx, userid, *message):

	try:
		userid = int(userid)
		user = ctx.guild.get_member(userid)
	except ValueError:
		await ctx.send(content='Specify target id')
		return
	message = ' '.join(message)
	hook = await ctx.guild.webhooks()
	hook = hook[0]
	await hook.send(content=message, username=user.nick, avatar_url=user.avatar_url)

@bot.command()
async def embed(ctx, *words):

	words = ' '.join(words)
	e = discord.Embed(title=ctx.author.name, description=words, color=0x523523)
	e.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=e)

@bot.command(aliases=['trans'])
async def translate(ctx, words, target='en', source='auto'):

	try:
		neword = trans.translate(words, dest=target, src=source)
	except ValueError:
		await ctx.send(content="Usage: `.translate 'words' destination(optional) source(optional)`")
		return
	e = discord.Embed(color=0x000055, title='Translator')
	e.add_field(name='Translated from {}'.format(neword.src), value=neword.text)
	await ctx.send(embed=e)

@bot.command()
async def ytdl(ctx, link):

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

@bot.command(aliases=['dictionary'])
async def dic(ctx, *words):

	words = '%20'.join(words)
	async with ctx.channel.typing():
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://www.dictionary.com/browse/{words}') as resp:
				soup = BeautifulSoup(await resp.text(), 'html.parser')
				try:
					subject = soup.h1.string
				except AttributeError:
					await ctx.send("Cant find word")
					return
				meaning = soup.find_all('span', class_='one-click-content css-1p89gle e1q3nk1v4')[0].get_text()	
				e = discord.Embed(title=subject, description=meaning, color=0x441400)
				await ctx.send(embed=e)

@bot.command()
async def nh(ctx, kw):

	html = requests.get('https://nhentai.net')
	soup = BeautifulSoup(html.text, 'html.parser')
	for title in soup.find_all('div', class_="caption")[5:]:
		if kw in title.string.lower():
			halfurl = title.parent.get('href')
			await ctx.send(content=f'https://nhentai.net{halfurl}')
			
@bot.command()
async def funa(ctx)
	
	funachar = str(random.randint(1, 400)).zfill(4)
	c_link = 'http://funamusea.com/character/img/{0}.html'.format(funachar)
	funa = requests.get('http://funamusea.com/character/{0}.html'.format(funachar))
	soup = BeautifulSoup(funa.text, 'html.parser')
	try:
		cname_en = soup.find('div', class_='c_name2').string
		cname_jp = soup.find('div', class_='c_name').string
	except AttributeError:
		await ctx.send("Your roll failed, roll again")
	e = discord.Embed(color=fc8c03, title=cname_en, description=cname_jp)
	e.set_image(url=c_link) 

@bot.command(help=hell['ping'])
async def ping(ctx):

	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
