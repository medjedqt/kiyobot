import discord
import asyncio
from discord.ext import commands
from kiyo import burnlist
from random import choice, randint
from discord.ext.commands import CommandNotFound,MissingRequiredArgument
from pybooru import Danbooru
import requests
import shutil
from os import listdir
from os.path import isfile, join
import os
from helpy import hell
import tension
from validator_collection import checkers
import process

bot = commands.Bot(command_prefix='?',case_insensitive=True)
bot.remove_command('help')
db = Danbooru('danbooru',username='hidevlad',api_key='VVPDr4B2k1m4CRDQHePcTYCF')
cloudir = "/app/cloud"
cloudirs = "/app/cloud/"
token = os.environ['BOT_TOKEN']

@bot.event
async def on_ready():

	print('We have logged in as {0.user}'.format(bot))
	bot.loop.create_task(status_task())

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
	elif isinstance(error, MissingRequiredArgument):
		await ctx.send(content="Missing arguments!")
		return
	raise error

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

	if key == None:
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
		if title == None:
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

'''@bot.command(aliases=['del'])
async def delete(ctx, file):

	try:
		await ctx.send(content="Are you sure? `y/n`")
		def check(chk):
			return chk.author == ctx.author and chk.channel == ctx.channel
		msg = await bot.wait_for('message',check=check,timeout=15)
		if msg.content in ("y", "Y"):
			os.remove(cloudirs+file)
			await ctx.send(content="Deleted {0}".format(file))
		elif msg.content in ("n", "N"):
			await ctx.send(content="Cancelled")
		else:
			await ctx.send(content="Unknown Input")
	except asyncio.TimeoutError:
		await ctx.send(content="Too slow!")'''

@bot.command()
async def connect(ctx):

	channel = ctx.author.voice.channel
	await channel.connect()
	await ctx.send("*hacker voice* I'M IN")

@bot.command(aliases=['dc'])
async def disconnect(ctx):

	await ctx.voice_client.disconnect()
	await ctx.send("bye...")
'''
@bot.command()
async def update(ctx, link):

	if checkers.is_url(link) == True:
		burnlist.append(link)
		with open('burnt.txt', 'w') as f:
			f.write(burnlist)
	else:
		print("unnice")

@bot.command()
async def reboot(ctx):

	bot.clear()
	channel = bot.get_channel(612588170676142081)
	await bot.send(content="Rebooted!",channel=channel)
'''
@bot.command()
async def ping(ctx):

	await ctx.send(content=":ping_pong: Pong!")

bot.run(token)
