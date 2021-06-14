import discord
from discord.ext import commands, menus

import fandom as fan
from fandom import FandomPage

class Fandom_Menu(menus.Menu):
	def __init__(self, page: FandomPage):
		self.page = page
		self.n = 0
		super().__init__(timeout=600,clear_reactions_after=True)
	
	async def send_initial_message(self, ctx, channel):
		e = discord.Embed(title=self.page.title, description=self.page.summary, url=self.page.url)
		e.add_field(name=self.page.sections[0], value=self.page.section(self.page.sections[0]))
		await channel.send(embed=e)

	@menus.button('▶')
	async def next_(self, payload):
		self.n += 1
		if self.n >= len(self.page.sections):
			self.n = 0
		name = self.page.sections[self.n]
		e = discord.Embed(title=self.page.title, description=self.page.summary, url=self.page.url)
		e.add_field(name=name, value=self.page.section(name))
		await self.message.edit(embed=e)

class Fandom(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command()
	async def fandom(self, ctx: commands.Context, fandom_community: str, *, item: str):
		try:
			name = fan.search(query='item', wiki=fandom_community, results=1)[0][0]
		except IndexError:
			await ctx.send(content="Can't find item")
		page = fan.page(title=name, wiki=fandom_community, preload=True)
		m = Fandom_Menu(page)
		await m.start(ctx)

def setup(bot: commands.Bot):
	bot.add_cog(Fandom(bot))