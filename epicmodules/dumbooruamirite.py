import discord
from discord.ext import commands
from random import randint, choice
import os
from pybooru import Danbooru
from helpy import hell

dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)

class Danboorushit(commands.Cog, name='Danbooru'):
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