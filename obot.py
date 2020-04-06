import discord
import asyncio
from discord.ext import commands
from kiyo import burnlist, lines
from random import choice, randint, uniform
from discord.ext.commands import CommandNotFound,MissingRequiredArgument
from pybooru import Danbooru
import requests
import shutil
from os import listdir
from os.path import isfile, join
import os
from helpy import hell
import tension
from googlesearch import search
import aiohttp
import io
import math


bot = commands.Bot(command_prefix='?',case_insensitive=True)
bot.remove_command('help')
token = os.environ['BOT_TOKEN']
dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)
cloudir = "/app/cloud"
cloudirs = "/app/cloud/"
logchan = 693130723015524382
messagechan = [612306757145853953]

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
	reactluck = uniform(0, 1.0)
	if message.author.bot or message_text.startswith('?'):
		pass
	elif 'CHEATING' in message_text:
		await message.channel.trigger_typing()
		await asyncio.sleep(3)
		await message.channel.send('Do I smell a liar in here?')
	elif message.author.id == 293395455830654977 and reactluck >= 0.85:
		await message.add_reaction('❤️')
	elif bot.user.mentioned_in(message):
		luck = randint(0,9)
		if message.author.id == 293395455830654977 and luck >= 7:
			e=discord.Embed(color=0xffff00)
			e.set_image(url="https://cdn.discordapp.com/attachments/569845300244774924/692219666478923776/23a8b2e1-21d4-4dac-84ba-1128207f0e30.png")
			await message.channel.send(embed=e)
		else:
			await message.channel.send(choice(lines))
	elif isinstance(message.channel,discord.DMChannel):
		channel = bot.get_channel(logchan)
		if message.attachments != []:
			att = message.attachments[0]
			fileurl = att.url
			if fileurl.find('/'):
				name=fileurl.rsplit('/',1)[1]
			async with aiohttp.ClientSession() as session:
				async with session.get(fileurl) as resp:
					if resp.status != 200:
						return await channel.send('Could not download file...')
					data = io.BytesIO(await resp.read())
					await channel.send(content='{0.author.name} said {0.content}'.format(message),file=discord.File(data, 'cool_image.png'))
		else:
			await channel.send(content='{0.author.name} said {0.content}'.format(message))
	await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):

	if before.author.bot or before.content == after.content or message.guild.id is not 569845300244774922:
		return
	channel = bot.get_channel(logchan)
	e = discord.Embed(title=before.author.name, color=0xff0000)
	e.add_field(name="Edited", value='"{0.content}" to "{1.content}"'.format(before,after))
	await channel.send(embed=e)

@bot.command()
async def help(ctx):

	e = discord.Embed(title="**__Basic Commands__**",color=0x00ff00)
	e.add_field(name="User Commands", value=hell, inline=False)
	await ctx.author.send(embed=e)

@bot.command()
async def burn(ctx):

	x = []
	x = burnlist
	e=discord.Embed(color=0xff0000)
	e.set_image(url=choice(burnlist))
	await ctx.send(embed=e)

@bot.command()
async def step(ctx):

	e=discord.Embed(color=0xffff00)
	e.set_image(url="https://cdn.discordapp.com/attachments/611844054669328394/635200592364699649/IMG_20191020_024438.JPG")
	await ctx.send(embed=e)
	
@bot.command(aliases=['nword','nw'])
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

@bot.command()
async def facto(ctx,num):

	satan = math.factorial(int(num))
	await ctx.send(content='{0}'.format(satan))

@bot.command()
async def dm(ctx,user: discord.User, msg):
	
	target = bot.get_user(user.id)
	await ctx.message.delete()
	await target.send(content=msg)
	
@bot.command(aliases=['k','kiyohime'])
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

@bot.command()
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

@bot.command(aliases=['danbooru','d'])
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
		
@bot.command()
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

@bot.command(aliases=['u','up'])
async def upload(ctx,title=None):

	try:
		ass =ctx.message.attachments[0]
		fileurl=ass.url
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
				shutil.move(newname,cloudir)
				await ctx.send(content="Uploaded as {0}".format(newname))
	except:
		await ctx.send(content="Attach a file!")

@bot.command(aliases=['dl','down'])
async def download(ctx,file):

	ind = {}
	x = [f for f in listdir(cloudirs) if isfile(join(cloudirs, f))]
	e = discord.Embed(color=0x00ffff)
	for i in x:
		name, ext = os.path.splitext(i)
		ind[i]= name
	for truepath, truename in ind.items():
		if file in truename:
			try:
				await ctx.send(file=discord.File(cloudirs + truepath))
			except:
				await ctx.send(content="File too big, please contact bot owner")

@bot.command(aliases=['ls'])
async def list(ctx):

	x = [f for f in listdir(cloudir) if isfile(join(cloudir, f))]
	e = discord.Embed(color=0x00ffff)
	for i in x:
		name, ext = os.path.splitext(i)
		next = tension.Ext(ext)
		e.add_field(name=i,value=next,inline=False)
	await ctx.send(embed=e)

@bot.command()
async def rename(ctx, oldname, newname):

	try:
		os.rename(cloudirs+oldname, cloudirs+newname)
		await ctx.send(content="Renamed {0} to {1}!".format(oldname, newname))
	except:
		await ctx.send(content="Invalid name")

@bot.command()
async def connect(ctx):

	channel = ctx.author.voice.channel
	await channel.connect()
	await ctx.send("*hacker voice* I'M IN")

@bot.command(aliases=['dc'])
async def disconnect(ctx):

	await ctx.voice_client.disconnect()
	await ctx.send("bye...")

@bot.command()
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

@bot.command()
async def tts(ctx, *msg):
	
	msg = ' '.join(msg)
	msga = await ctx.send(content=msg, tts=True)
	await msga.delete()
	await ctx.message.delete()

@bot.command()
async def door(ctx):
	
	r = requests.get('https://medjed.fun')
	if r.status_code == 200:
		await ctx.send(content="Door is open")
	else:
		await ctx.send(content="A problem has occured")	

@bot.command()
async def google(ctx,*query):
	
	query = ''.join(query)
	for result in search(query, tld='com', num=1, stop=1, pause=2):
		await ctx.send(result)

@bot.command()
async def ping(ctx):

	await ctx.send(content=":ping_pong: Pong!")
	
bot.run(token)
