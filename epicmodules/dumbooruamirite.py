import discord
from discord.ext import commands
from random import randint, choice
import os
from helpy import hell
from sauce_finder import sauce_finder

class Danboorushit(commands.Cog, name='Danbooru'):
	def __init__(self, bot, db):
		self.bot = bot
		self.db = db
	
	@commands.command(help=hell['latest'])
	async def latest(self, ctx, key=None, *tag):

		if key is None:
			tag="kiyohime_(fate/grand_order)"
		else:
			tag = '_'.join(tag)
			tag = key + '_' + tag
		posts = self.db.post_list(tags=tag, page=1, limit=1)
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

		newtag = '_'.join(tag)
		page = randint(1,5)
		try:
			posts = self.db.post_list(tags=newtag,page=page,limit=5)
			post = choice(posts)
			try:
				fileurl = post['file_url']
			except KeyError:
				fileurl = 'https://danbooru.donmai.us' + post['source']
			e = discord.Embed(color=0x0000ff)
			e.set_image(url=fileurl)
			await ctx.send(embed=e)
		except:
			await ctx.send(content="Can't find image! Please enter in this format `character name (series)`")

	@commands.command(help=hell['multi'])
	async def multi(self, ctx, *tag):

		tag = ' '.join(tag)
		page = randint(1,5)
		e = discord.Embed(color=0x00FFBE)
		try:
			posts = self.db.post_list(tags=tag,page=page,limit=5)
			for post in posts:
				try:
					fileurl = post['file_url']
				except KeyError:
					fileurl = 'https://danbooru.donmai.us' + post['source']
				e.set_image(url=fileurl)
				await ctx.send(embed=e)
		except:
			await ctx.send(content="Some shit broke. Also firara is gay")
	
	@commands.command()
	async def sauce(self, ctx):
		url = ctx.message.attachments[0].url
		result = sauce_finder.get_match(url)
		if result['type'] == 'possible':
			thing = result['found'][0]['link']
		else:
			thing = result['found']['link']
		await ctx.send(content=f"{result['type']} result: {thing}")