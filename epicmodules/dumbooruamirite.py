import asyncio
import discord
from discord.ext import commands, menus
from random import randint, choice
from requests.exceptions import HTTPError
from sauce_finder import sauce_finder
from hentai import Hentai, Format, Utils, Sort

class DoujinMenu(menus.Menu):
	def __init__(self, ctx, bot, dj):
		super().__init__(timeout=600, clear_reactions_after=True)
		self.dj: Hentai = dj
	
	async def send_initial_message(self, ctx, channel):
		return await channel.send(content=self.dj.image_urls[0])

	@menus.button('◀')
	async def left(self, payload):
		nindex = self.dj.image_urls.index(self.message.content) - 1
		if nindex == -1:
			nindex = len(self.dj.image_urls) - 1
		await self.message.edit(content=self.dj.image_urls[nindex])

	@menus.button('▶')
	async def right(self, payload):
		nindex = self.dj.image_urls.index(self.message.content) + 1
		if nindex == len(self.dj.image_urls):
			nindex = 0
		await self.message.edit(content=self.dj.image_urls[nindex])
	
	@menus.button('❌')
	async def clear(self, payload):
		self.stop()
class Danboorushit(commands.Cog, name='Danbooru'):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.db = bot.db

	@commands.command()
	async def latest(self, ctx: commands.Context, key: str = None, *tag: str):
		'''shits out latest danbooru pic (kiyo by default)'''
		if key is None:
			tag="kiyohime_(fate/grand_order)"
		else:
			tag = '_'.join(tag)
			tag = key + '_' + tag
		post = self.db.post_list(tags=tag, page=1, limit=1)[0]
		if post['rating'] != 's' and not (ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel)):
			return await ctx.send("Command returned an NSFW result in an SFW channel :<")
		try:
			fileurl = post['file_url']
		except KeyError:
			fileurl = 'https://danbooru.donmai.us' + post['source']
		e = discord.Embed(title="Latest", color=0x00FF00)
		e.set_image(url=fileurl)
		await ctx.send(embed=e)

	@commands.command(aliases=['dan','d'])
	async def danbooru(self, ctx: commands.Context, *tag: str):
		'''Finds an image on danbooru'''
		page = randint(1,5)
		try:
			posts = self.db.post_list(tags=tag,page=page,limit=5)
			post = choice(posts)
			if post['rating'] != 's' and not (ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel)):
				return await ctx.send("Command returned an NSFW result in an SFW channel :<")
			try:
				fileurl = post['file_url']
			except KeyError:
				fileurl = 'https://danbooru.donmai.us' + post['source']
			e = discord.Embed(color=0x0000ff)
			e.set_image(url=fileurl)
			await ctx.send(embed=e)
		except IndexError:
			correctlist = list()
			for t in tag:
				q = '*'+t+'*'
				correct = self.db.tag_list(order='count', name_matches=q)
				correctlist+=correct
			if correctlist:
				await ctx.send(content="Can't find tag, did you mean;")
				for i, correct in enumerate(correctlist):
					if i == 5:
						break
					await ctx.send(content=correct['name'])
			else:
				await ctx.send(content="Can't find image! Please enter in this format `character name (series)`")

	@commands.command()
	async def multi(self, ctx: commands.Context, *, tag: str):
		'''Finds multiple images on danbooru'''
		page = randint(1,5)
		e = discord.Embed(color=0x00FFBE)
		try:
			posts = self.db.post_list(tags=tag,page=page,limit=5)
			
			for post in posts:
				if post['rating'] != 's' and not (ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel)):
					return await ctx.send("Command returned an NSFW result in an SFW channel :<")
				else:
					try:
						fileurl = post['file_url']
					except KeyError:
						fileurl = 'https://danbooru.donmai.us' + post['source']
					e.set_image(url=fileurl)
					await ctx.send(embed=e)
		except IndexError:
			correctlist = list()
			q = '*'+tag+'*'
			correct = self.db.tag_list(order='count', name_matches=q)
			correctlist+=correct
			if correctlist:
				await ctx.send(content="Can't find tag, did you mean;")
				for i, correct in enumerate(correctlist):
					if i == 5:
						break
					await ctx.send(content=correct['name'])
			else:
				await ctx.send(content="Some shit broke. Also firara is gay")
	
	@commands.command()
	async def iqdb(self, ctx: commands.Context, url: str = None):
		'''finds image sauce on iqdb'''
		if url is None:
			url = ctx.message.attachments[0].url
		elif url is None and ctx.message.reference:
			url = ctx.message.reference.resolved.attachments[0].url
		result = sauce_finder.get_match(url)
		if result['type'] == 'possible':
			thing = result['found'][0]
		else:
			thing = result['found']
		if thing['rating'] == '[Explicit]' and not (ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel)):
			await ctx.send("Explicit result")
			return
		await ctx.send(content=f"{result['type']} result: {thing['link']}")

	@commands.command(aliases=['nao', 'sauce'])
	async def saucenao(self, ctx: commands.Context, url: str = None):
		'''finds image sauce on saucenao'''
		if url is None and ctx.message.attachments:
			url = ctx.message.attachments[0].url
		elif url is None and ctx.message.reference:
			url = ctx.message.reference.resolved.attachments[0].url
		results = await self.bot.sauce.from_url(url)
		if len(results) == 0:
			await ctx.send(content="No results found.")
			return
		await ctx.send(content=f'Similarity: {results[0].similarity}\n{results[0].url}')
	
	@commands.is_nsfw()
	@commands.group(aliases=['nh'], invoke_without_command=True)
	async def nhentai(self, ctx: commands.Context, djid = None, *, extra: str = ''):
		'''finds doujins on nhentai by id'''
		if ctx.invoked_subcommand is not None:
			return
		if djid is None:
			await ctx.send_help(ctx.command)
			return
		if not Hentai.exists(djid):
			return await self.search(ctx, tags=f'{djid} {extra}')
		result = Hentai(djid)
		tags = [_.name for _ in result.tag]
		e = discord.Embed(title=result.title(Format.Pretty), description=f'#{result.id}', url=result.url, color=int(djid))
		e.set_image(url=result.cover)
		e.set_footer(text=result.upload_date)
		e.add_field(name="Tags", value=', '.join(tags))
		artists = ', '.join([_.name for _ in result.artist]) if result.artist != [] else 'None'
		e.add_field(name="Artist(s)",value=artists)
		await ctx.send(embed=e)
	
	@nhentai.error
	async def nh_error(self, ctx: commands.Context, error):
		if isinstance(error, ValueError):
			rep = ctx.message.content.replace(f'{ctx.prefix}{ctx.invoked_with}', f'{ctx.prefix}{ctx.invoked_with} search')
			await ctx.send(f"Invalid doujin id, did you mean `{rep}`")

	@commands.is_nsfw()
	@nhentai.command()
	async def random(self, ctx: commands.Context):
		'''finds random doujin'''
		await self.nhentai(ctx, Utils.get_random_id())

	async def _search(self, ctx: commands.Context, tags: str, sort):
		res = Utils.search_by_query(tags, sort=sort)
		if res != []:
			msg = "Choose from `1-5`;\n"
			for i, dj in enumerate(res):
				if i < 5:
					msg+=f"{i+1}: {dj.title(Format.English)}\n"
			mes: discord.Message = await ctx.send(content=msg)
		else:
			await ctx.send('No results found!')
			return
		def check(inp: discord.Message):
			return inp.author == ctx.author
		try:
			msg: discord.Message = await self.bot.wait_for('message', check=check, timeout=30.0)
			djid = res[int(msg.content)-1].id
			await self.nhentai(ctx, djid)
		except (ValueError, IndexError):
			await mes.delete()
			await ctx.send("Invalid input")
		except asyncio.TimeoutError:
			await mes.delete()

	@commands.is_nsfw()
	@nhentai.group(aliases=['find'], invoke_without_command=True)
	async def search(self, ctx: commands.Context, *, tags: str):
		'''finds doujins by tags'''
		await self._search(ctx, tags, Sort.Popular)
	
	@commands.is_nsfw()
	@search.command(aliases=['lat', 'recent', 'newest', 'new'])
	async def latest(self, ctx: commands.Context, *, tags: str):
		'''finds latest doujins'''
		await self._search(ctx, tags, Sort.Date)

	@commands.is_nsfw()
	@search.command(aliases=['T', 'D', 'tdy'])
	async def today(self, ctx: commands.Context, *, tags: str):
		'''finds popular doujins today'''
		await self._search(ctx, tags, Sort.PopularToday)

	@commands.is_nsfw()
	@search.command(aliases=['W', 'wk'])
	async def week(self, ctx: commands.Context, *, tags: str):
		'''finds popular doujins this week'''
		await self._search(ctx, tags, Sort.PopularWeek)

	@commands.is_nsfw()
	@search.command(aliases=['M', 'mon'])
	async def month(self, ctx: commands.Context, *, tags: str):
		'''finds popular doujins this month'''
		await self._search(ctx, tags, Sort.PopularMonth)

	@commands.is_nsfw()
	@search.command(aliases=['Y', 'yr'])
	async def year(self, ctx: commands.Context, *, tags: str):
		'''finds popular doujins this year'''
		await self._search(ctx, tags, Sort.PopularYear)

	@commands.is_nsfw()
	@nhentai.command(name='read')
	async def _read(self, ctx: commands.Context, djid: int):
		'''opens a reader '''
		try:
			dj = Hentai(djid)
		except HTTPError:
			return await ctx.send(content='Invalid code')
		m = DoujinMenu(ctx, self.bot, dj)
		await m.start(ctx)

def setup(bot: commands.Bot):
	bot.add_cog(Danboorushit(bot))