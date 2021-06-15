import discord
from discord.ext import commands, menus

import fandom as fan
from fandom import FandomPage

class Fandom_Menu(menus.Menu):
	def __init__(self, page: FandomPage):
		self.page = page
		self.summary = page.summary
		if len(self.summary)>200:
			self.summary = self.summary[:150]+"..."
		self.title = page.title
		self.url = page.url
		self.footer = page.wiki
		self.n = 0
		super().__init__(timeout=600,clear_reactions_after=True)
	
	async def send_initial_message(self, ctx, channel):
		e = discord.Embed(title=self.title, description=self.summary, url=self.url)
		name = self.page.sections[0]
		value = self.page.section(name)
		if len(value)>1000:
			value = value[:1000]+'...'
		e.add_field(name=name, value=value)
		e.set_footer(text=self.footer)
		return await channel.send(embed=e)

	async def change_page(self):
		name = self.page.sections[self.n]
		value = self.page.section(name)
		if len(value) > 1000:
			value = value[:1000]+'...'
		e = discord.Embed(title=self.title, description=self.summary, url=self.url)
		e.add_field(name=name, value=value)
		e.set_footer(text=self.footer)
		await self.message.edit(embed=e)

	@menus.button('◀')
	async def left(self, payload):
		self.n -= 1
		if self.n == -1:
			self.n = len(self.page.sections) - 1
		await self.change_page()

	@menus.button('▶')
	async def right(self, payload):
		self.n += 1
		if self.n >= len(self.page.sections):
			self.n = 0
		await self.change_page()
	
	@menus.button('❌')
	async def clear(self, payload):
		self.stop()

class Fandom(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command()
	async def fandom(self, ctx: commands.Context, fandom_community: str, *, item: str):
		try:
			name = fan.search(query=item, wiki=fandom_community, results=1)[0][0]
		except IndexError:
			await ctx.send(content="Can't find item")
		page = fan.page(title=name, wiki=fandom_community, preload=True)
		m = Fandom_Menu(page)
		await m.start(ctx)

def setup(bot: commands.Bot):
	bot.add_cog(Fandom(bot))