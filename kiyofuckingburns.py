import discord
from discord.ext import commands
from random import randint, choice
from kiyo import burnlist
from pybooru import Danbooru
import os

dbkey = os.environ['DAN_KEY']
dbname = os.environ['DAN_NAME']
db = Danbooru('danbooru',username=dbname,api_key=dbkey)

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