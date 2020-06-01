import discord
import asyncio
from kiyo import burnlist, lines, rpsfunc
from random import choice, randint, uniform
from discord.ext.commands import CommandNotFound,MissingRequiredArgument
from pybooru import Danbooru
import requests
import shutil
from os import listdir, path
import os
from helpy import hell
import tension
from googlesearch import search
import aiohttp
import io
import math
from mathe import calculate
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


bot = discord.ext.commands.Bot(command_prefix='?',case_insensitive=True)
bot.remove_command('help')
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)
cloudir = "/app/cloud"
cloudirs = "/app/cloud/"
logchan = 693130723015524382
messagechan = [612306757145853953]
rpslist = ['rock', 'paper', 'scissors']
gauth = GoogleAuth()
gauth.LoadCredentialsFile("auth.json")
if gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()
drive = GoogleDrive(gauth)
browser = webdriver.Chrome()
browser.get('https://www.cleverbot.com')


@bot.event
async def on_ready():

	print('We have logged in as {0.user}'.format(bot))
	bot.loop.create_task(status_task())
	channel = bot.get_channel(logchan)
	await channel.send(content='Restarted')

async def status_task():

	while True:
		await bot.change_presence(activity=discord.Game(name="with Fira's pussy"))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Activity(name="Fira nutting to me", type=discord.ActivityType.watching))
		await asyncio.sleep(8)
		await bot.change_presence(activity=discord.Game(name="?help"))
		await asyncio.sleep(8)

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, CommandNotFound):
		return
	if isinstance(error, MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
		return
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
			async with aiohttp.ClientSession() as session:
				async with session.get(fileurl) as response:
					if response.status != 200:
						return await channel.send('Could not download file...')
					data = io.BytesIO(await response.read())
					e.add_field(name=sender, value=message.content)
					await channel.send(embed=e,file=discord.File(data, 'image.png'))
		else:
			e.add_field(name=sender, value=message.content)
			await channel.send(embed=e)
	await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):

	if before.author.bot or before.content == after.content or before.guild.id != 569845300244774922:
		return
	channel = bot.get_channel(logchan)
	e = discord.Embed(title=before.author.name, color=0xff0000)
	e.add_field(name="Edited", value='"{0.content}" to "{1.content}"'.format(before,after))
	await channel.send(embed=e)

#@bot.command(enabled=False)
#async def help(ctx):

#	e = discord.Embed(title="**__Basic Commands__**",color=0x00ff00)
#	e.add_field(name="User Commands", value=hell, inline=False)
#	await ctx.author.send(embed=e)

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
async def say(ctx, msg, time=5, count=1):

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
async def calc(ctx, func, arg=None, arg2=None):

	function = calculate[func]
	if arg2 is None:
		result = function(int(arg))
	else:
		result = function(int(arg),int(arg2))
	await ctx.send(content=result)

@bot.command()
async def rps(ctx, userid, move):

	if isinstance(ctx.channel,discord.DMChannel) and move in rpslist:
		target = bot.get_user(int(userid))
		await ctx.send(content="Challenged {}".format(target.name))
		await target.send(content='{} challenged you to a rock paper scissors! Reply with your move (Rock/Paper/Scissors)'.format(ctx.author.name))
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
			if text.startswith(('.','f.','!','<','-','?','$','_')):
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
async def chat(ctx, *question):

	q = ' '.join(question)
	async with ctx.channel.typing():
		inputbox = browser.find_element_by_name('stimulus')
		inputbox.clear()
		inputbox.send_keys(q)
		inputbox.send_keys(Keys.RETURN)
		await asyncio.sleep(2)
		before = browser.find_element_by_xpath("//p[@id='line1']/span").text
		while before != browser.find_element_by_xpath("//p[@id='line1']/span").text:
			await asyncio.sleep(3)
			before = browser.find_element_by_xpath("//p[@id='line1'/span").text
		#if response.text == '':
		await ctx.send(content=before)

@bot.command(help=hell['ping'])
async def ping(ctx):

	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
