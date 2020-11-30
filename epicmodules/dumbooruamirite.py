import discord
from discord.ext import commands
from random import randint, choice
from helpy import hell
from sauce_finder import sauce_finder

class Danboorushit(commands.Cog, name='Danbooru'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.db = bot.db
	
	@commands.is_nsfw()
	@commands.command(help=hell['latest'])
	async def latest(self, ctx: commands.Bot, key: str = None, *tag: list[str]):

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
	
	@commands.is_nsfw()
	@commands.command(aliases=['danbooru','d'],help=hell['danbooru'])
	async def dan(self, ctx: commands.Context, *tag: list[str]):

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

	@commands.is_nsfw()
	@commands.command(help=hell['multi'])
	async def multi(self, ctx: commands.Context, *, tag: str):

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
	async def iqdb(self, ctx: commands.Context, url: str = None):
		if url is None:
			url = ctx.message.attachments[0].url
		result = sauce_finder.get_match(url)
		if result['type'] == 'possible':
			thing = result['found'][0]
		else:
			thing = result['found']
		if thing['rating'] == '[Explicit]' and not ctx.channel.is_nsfw():
			await ctx.send("Explicit result")
			return
		await ctx.send(content=f"{result['type']} result: {thing['link']}")

	@commands.command(aliases=['nao', 'sauce'])
	async def saucenao(self, ctx: commands.Context, url: str = None):
		if url is None:
			url = ctx.message.attachments[0].url
		results = await self.bot.sauce.from_url(url)
		if len(results) == 0:
			await ctx.send(content="No results found.")
			return
		await ctx.send(content=f'Similarity: {results[0].similarity}\n{results[0].url}')

def setup(bot: commands.Bot):
	bot.add_cog(Danboorushit(bot))